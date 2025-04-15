import asyncio
import io
import logging
from base64 import b64decode
from dataclasses import dataclass
from typing import AsyncIterator
from uuid import uuid4

import aiohttp
import tornado
from PIL import Image
from tornado.escape import json_decode, json_encode
from tornado.httpclient import HTTPRequest
from tornado.ioloop import PeriodicCallback
from tornado.websocket import WebSocketClientConnection, websocket_connect

logger = logging.getLogger(__name__)

# matplotlib 설정 상수
# 그래프의 기본 크기 (가로, 세로) - 인치 단위
# 10x6 인치는 웹 환경에서 보기 좋은 와이드스크린 비율입니다
FIGURE_SIZE = (10, 6)

# 그래프 저장 시 기본 파일 형식
# 'svg': 벡터 그래픽 형식으로 확대해도 품질이 저하되지 않음
# 다른 옵션: 'png', 'pdf', 'jpg' 등
SAVEFIG_FORMAT = "svg"

# IPython에서 표시할 그래프 형식 목록
# 여러 형식을 지정하면 모두 생성되어 클라이언트에서 선택 가능
# 'svg': 벡터 그래픽으로 확대/축소 및 동적 조작에 적합
# 'png': 래스터 이미지로 모든 환경에서 일관된 표시 가능
MATPLOTLIB_FORMATS = ["svg", "png"]


class ConnectionError(Exception):
    """Exception raised when connection to an IPython kernel fails."""

    pass


class ExecutionError(Exception):
    """Exception raised when code execution in the IPython kernel fails.

    Args:
        message: Error message
        trace: Stack trace string representation
    """

    def __init__(self, message: str, trace: str | None = None):
        super().__init__(message)
        self.trace = trace


@dataclass
class ExecutionResult:
    """The result of a code execution.

    Args:
        text: Output text generated during execution
        images: List of images generated during execution
        svg_images: List of SVG XML strings generated during execution
    """

    text: str | None
    images: list[str]


class Execution:
    """Represents a code execution in an IPython kernel.

    Args:
        client: The client instance that created this execution
        req_id: Unique identifier for the execution request
    """

    def __init__(self, client: "ExecutionClient", req_id: str):
        self.client = client
        self.req_id = req_id

        self._chunks: list[str] = []
        self._images: list[str] = []

        self._stream_consumed: bool = False

    async def result(self, timeout: float = 120) -> ExecutionResult:
        """Waits for execution to complete and returns the final result.

        If a timeout is reached, the kernel is interrupted.

        Args:
            timeout: Maximum time to wait in seconds. Defaults to 120.

        Returns:
            ExecutionResult object

        Raises:
            asyncio.TimeoutError: If execution exceeds timeout duration
        """
        if not self._stream_consumed:
            async for _ in self.stream(timeout=timeout):
                pass

        return ExecutionResult(
            text="".join(self._chunks).strip() if self._chunks else None,
            images=self._images,
        )

    async def stream(self, timeout: float = 120) -> AsyncIterator[str]:
        """Streams the execution output text as it becomes available.

        Args:
            timeout: Maximum time to wait in seconds. Defaults to 120.

        Yields:
            Output text chunks as they arrive

        Raises:
            asyncio.TimeoutError: If execution exceeds timeout duration
        """
        try:
            async with asyncio.timeout(timeout):
                async for elem in self._stream():
                    match elem:
                        case str():
                            self._chunks.append(elem)
                            yield elem
        except asyncio.TimeoutError:
            await self.client._interrupt_kernel()
            await asyncio.sleep(0.2)  # TODO: make configurable
            raise
        finally:
            self._stream_consumed = True

    async def _stream(self) -> AsyncIterator[str]:
        while True:
            msg_dict = await self.client._read_message()
            msg_type = msg_dict["msg_type"]
            msg_id = msg_dict["parent_header"].get("msg_id", None)

            if msg_id != self.req_id:
                continue

            if msg_type == "stream":
                yield msg_dict["content"]["text"]
            elif msg_type == "error":
                self._raise_error(msg_dict)
            elif msg_type == "execute_reply":
                if msg_dict["content"]["status"] == "error":
                    self._raise_error(msg_dict)
                break
            elif msg_type in ["execute_result", "display_data"]:
                msg_data = msg_dict["content"]["data"]
                yield msg_data["text/plain"]

                # SVG 형식 처리
                if "image/svg+xml" in msg_data:
                    svg_data = msg_data["image/svg+xml"]
                    self._images.append(svg_data)

    def _raise_error(self, msg_dict):
        error_name = msg_dict["content"].get("ename", "Unknown Error")
        error_value = msg_dict["content"].get("evalue", "")
        error_trace = "\n".join(msg_dict["content"]["traceback"])
        raise ExecutionError(f"{error_name}: {error_value}", error_trace)


class ExecutionClient:
    """A context manager for executing code in an IPython kernel.

    Args:
        host: Hostname where the code execution container is running
        port: Host port of the code execution container
        heartbeat_interval: Interval in seconds between heartbeat pings. Defaults to 10.

    Example:
        ```python
        from jarvis_ipybox import ExecutionClient, ExecutionContainer

        binds = {"/host/path": "example/path"}
        env = {"API_KEY": "secret"}

        async with ExecutionContainer(binds=binds, env=env) as container:
            async with ExecutionClient(host="localhost", port=container.port) as client:
                result = await client.execute("print('Hello, world!')")
                print(result.text)
        ```
        > Hello, world!
    """

    def __init__(
        self,
        port: int,
        host: str = "localhost",
        heartbeat_interval: float = 10,
        https: bool = False,
        kernel_id: str = None
    ):
        self.port = port
        self.host = host
        self.https = https

        self._heartbeat_interval = heartbeat_interval
        self._heartbeat_callback = None

        self._kernel_id = kernel_id
        self._ws: WebSocketClientConnection

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    @property
    def kernel_id(self):
        """The ID of the running IPython kernel.

        Raises:
            ValueError: If not connected to a kernel
        """
        if self._kernel_id is None:
            raise ValueError("Not connected to kernel")
        return self._kernel_id

    @property
    def base_http_url(self):
        if self.https:
            return f"https://{self.host}:{self.port}/api/kernels"
        else:
            return f"http://{self.host}:{self.port}/api/kernels"

    @property
    def kernel_http_url(self):
        return f"{self.base_http_url}/{self.kernel_id}"

    @property
    def kernel_ws_url(self):
        if self.https:
            return f"wss://{self.host}:{self.port}/api/kernels/{self.kernel_id}/channels"
        else:
            return f"ws://{self.host}:{self.port}/api/kernels/{self.kernel_id}/channels"

    async def connect(self, retries: int = 10, retry_interval: float = 1.0):
        """Creates and connects to an IPython kernel.

        Args:
            retries: Number of connection attempts. Defaults to 10.
            retry_interval: Delay between retries in seconds. Defaults to 1.0.

        Raises:
            ConnectionError: If connection cannot be established after all retries
        """
        if self._kernel_id is None:
            for _ in range(retries):
                    try:
                        self._kernel_id = await self._create_kernel()
                        break
                    except Exception:
                        await asyncio.sleep(retry_interval)
            else:
                raise ConnectionError("Failed to create kernel")

        self._ws = await websocket_connect(HTTPRequest(url=self.kernel_ws_url))
        logger.info("Connected to kernel")

        self.heartbeat_callback = PeriodicCallback(
            self._ping_kernel, self._heartbeat_interval * 1000
        )
        self.heartbeat_callback.start()
        logger.info(f"Started heartbeat (interval = {self._heartbeat_interval}s)")

        await self._init_kernel()

    async def disconnect(self):
        """Closes the connection to the kernel and cleans up resources."""
        self.heartbeat_callback.stop()
        self._ws.close()
        # async with aiohttp.ClientSession() as session:
        #     async with session.delete(self.kernel_http_url):
        #         pass

    async def execute(self, code: str, timeout: float = 120) -> ExecutionResult:
        """Executes code and returns the result.

        Args:
            code: Code to execute
            timeout: Maximum execution time in seconds. Defaults to 120.

        Returns:
            ExecutionResult object

        Raises:
            ExecutionError: If code execution raised an error
            asyncio.TimeoutError: If execution exceeds timeout duration
        """
        execution = await self.submit(code)
        return await execution.result(timeout=timeout)

    async def submit(self, code: str) -> Execution:
        """Submits code for execution and returns an Execution object to track it.

        Args:
            code: Python code to execute

        Returns:
            An Execution object to track the submitted code execution
        """
        req_id = uuid4().hex
        req = {
            "header": {
                "username": "",
                "version": "5.0",
                "session": "",
                "msg_id": req_id,
                "msg_type": "execute_request",
            },
            "parent_header": {},
            "channel": "shell",
            "content": {
                "code": code,
                "silent": False,
                "store_history": False,
                "user_expressions": {},
                "allow_stdin": False,
            },
            "metadata": {},
            "buffers": {},
        }

        await self._send_request(req)
        return Execution(client=self, req_id=req_id)

    async def get_module_sources(self, module_names: list[str]) -> str | None:
        result = await self.execute(f"print_module_sources({module_names})")
        return result.text

    async def _send_request(self, req):
        await self._ws.write_message(json_encode(req))

    async def _read_message(self) -> dict:
        return json_decode(await self._ws.read_message())

    async def _create_kernel(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.base_http_url, json={"name": "python"}) as response:
                kernel = await response.json()
                return kernel["id"]

    async def _interrupt_kernel(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.kernel_http_url}/interrupt", json={"kernel_id": self._kernel_id}
            ) as response:
                logger.info(f"Kernel interrupted: {response.status}")

    async def _ping_kernel(self):
        try:
            self._ws.ping()
        except tornado.iostream.StreamClosedError as e:
            logger.error("Kernel disconnected", e)

    async def _init_kernel(self):
        await self.execute(
            r"%colors nocolor"
            + "\n# 필요한 모듈 임포트"
            + "\nfrom jarvis_ipybox.modinfo import print_module_sources, get_module_info"
            + "\nimport matplotlib"
            + "\nimport matplotlib.pyplot as plt"
            + "\nfrom matplotlib_inline.backend_inline import set_matplotlib_formats"
            + "\n# matplotlib 설정"
            # + "\nmatplotlib.use('Agg')"  # 백엔드 설정
            + f"\nplt.rcParams['figure.figsize'] = {FIGURE_SIZE}"
            + f"\nplt.rcParams['savefig.format'] = '{SAVEFIG_FORMAT}'"
            + f"\nset_matplotlib_formats({', '.join(repr(fmt) for fmt in MATPLOTLIB_FORMATS)})"
            + "\nmatplotlib.rc('font', family=['NanumGothic'])"
            + "\nmatplotlib.rcParams['axes.unicode_minus'] = False"
            + "\n# 폰트 크기 설정"
            + "\nmatplotlib.rcParams['font.size'] = 16  # 기본 폰트 크기"
            + "\nmatplotlib.rcParams['axes.titlesize'] = 24  # 그래프 제목 크기"
            + "\nmatplotlib.rcParams['axes.labelsize'] = 16  # 축 레이블 크기"
            + "\nmatplotlib.rcParams['xtick.labelsize'] = 16  # x축 눈금 레이블 크기"
            + "\nmatplotlib.rcParams['ytick.labelsize'] = 16  # y축 눈금 레이블 크기"
            + "\nmatplotlib.rcParams['legend.fontsize'] = 16  # 범례 폰트 크기"
        )
