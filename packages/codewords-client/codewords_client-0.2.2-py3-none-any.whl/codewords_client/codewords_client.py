import asyncio
import json
import os
import time
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Generator, Literal, Optional, Tuple, Union, overload

import httpx

###############################################################################
#                          RESPONSE WRAPPER CLASSES
###############################################################################


class AsyncCodewordsResponse:
    """
    A wrapper around a Codewords request_id that provides convenient methods
    for accessing logs and results.
    """

    def __init__(
        self,
        request_id: str,
        client: "AsyncCodewordsClient",
    ):
        self.request_id = request_id
        self._client = client

    def __repr__(self) -> str:
        return f"AsyncCodewordsResponse(request_id={self.request_id})"

    def __str__(self) -> str:
        return self.request_id

    async def logs(self) -> AsyncGenerator[dict, None]:
        """
        Returns an async generator of log lines for this request.

        Usage:
            response = await client.start_service(...)
            async for log_line in response.logs():
                print(log_line)

        Note: Automatically reconnects when connection times out (e.g., after App Runner's 120-second limit)
        """
        async for log in self._client.get_logs(self.request_id):
            yield log

    async def result(self, timeout_seconds: int = 300) -> httpx.Response:
        """
        Polls for the final result of this request until it's complete.

        :param timeout_seconds: Maximum time to wait for the result in seconds.
        :return: The complete request record, including response data.
        """
        return await self._client.poll_result(self.request_id, timeout_seconds)

    async def details(self) -> dict:
        """
        Gets the current details of this request.

        :return: The current request record.
        """
        return await self._client.get_request_details(self.request_id)


class CodewordsResponse:
    """
    A synchronous wrapper around a Codewords request_id that provides convenient methods
    for accessing logs and results.
    """

    def __init__(
        self,
        request_id: str,
        client: "CodewordsClient",
    ):
        self.request_id = request_id
        self._client = client

    def __repr__(self) -> str:
        return f"CodewordsResponse(request_id={self.request_id})"

    def __str__(self) -> str:
        return self.request_id

    def logs(self) -> Generator[dict, None, None]:
        """
        Returns a generator of log lines for this request.

        Usage:
            response = client.start_service(...)
            for log_line in response.logs():
                print(log_line)

        Note: Automatically reconnects when connection times out (e.g., after App Runner's 120-second limit)
        """
        yield from self._client.get_logs(self.request_id)

    def result(self, timeout_seconds: int = 300) -> httpx.Response:
        """
        Polls for the final result of this request until it's complete.

        :param timeout_seconds: Maximum time to wait for the result in seconds.
        :return: The complete request record, including response data.
        """
        return self._client.poll_result(self.request_id, timeout_seconds)

    def details(self) -> dict:
        """
        Gets the current details of this request.

        :return: The current request record.
        """
        return self._client.get_request_details(self.request_id)


###############################################################################
#                            ASYNC CODEWORDS CLIENT
###############################################################################


class AsyncCodewordsClient:
    """
    An async client for interacting with the Codewords runtime server.
    It reuses a single httpx.AsyncClient for all requests.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        default_timeout: float = 115.0,
    ):
        """
        :param base_url: Base URL of the Codewords runtime (e.g. 'https://runtime.codewords.ai').
                        If None, uses environment var `RUNTIME_URI` or fallback 'https://runtime.codewords.ai'.
        :param api_key: Your Codewords API key. If None, uses env var `CODEWORDS_API_KEY`.
        :param default_timeout: Default request timeout in seconds for all calls (except streams).
        """
        if base_url is None:
            base_url = os.getenv("RUNTIME_URI", "https://runtime.codewords.ai")

        if api_key is None:
            env_key = os.getenv("CODEWORDS_API_KEY")
            if not env_key:
                raise ValueError("CODEWORDS_API_KEY is not set")
            api_key = env_key

        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.default_timeout = default_timeout

        # Reuse one httpx.AsyncClient
        self.client = httpx.AsyncClient(timeout=self.default_timeout)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        try:
            await self.client.aclose()
        except Exception as e:
            print(f"Error closing client: {e}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def _auth_headers(self) -> Dict[str, str]:
        """
        Helper to build authorization headers.
        The server allows raw 'Authorization: cwk-...' or 'Bearer ...'
        """
        return {"Authorization": self.api_key}

    async def provision_request(self) -> str:
        """POST /provision-request to create a 'husk' request. Returns the new request_id."""
        url = f"{self.base_url}/provision-request"
        resp = await self.client.post(url, headers=self._auth_headers())
        resp.raise_for_status()
        return resp.json()["request_id"]

    @overload
    async def run(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        in_background: Literal[False] = False,
        run_as_template: Optional[bool] = False,
    ) -> httpx.Response: ...

    @overload
    async def run(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        in_background: Literal[True] = True,
        run_as_template: Optional[bool] = False,
    ) -> AsyncCodewordsResponse: ...

    async def run(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        in_background: bool = False,
        run_as_template: Optional[bool] = False,
    ) -> Union[httpx.Response, AsyncCodewordsResponse]:
        """
        POST /run/{service_id}/{path}, optionally using a pre-provisioned request ID.

        :param service_id: Target service ID.
        :param inputs: Payload sent in the POST body. If dict, sent as JSON; str => text; bytes => raw.
        :param path: Optional path appended after service_id (e.g. 'predict' => /run/{service_id}/predict).
        :param request_id: If provided, sends as 'X-Provisioned-Request-Id'.
                           Otherwise, the server auto-creates a new ephemeral request.
        :param correlation_id: If provided, sends as 'X-Correlation-Id'.
        :param in_background: If True, returns a tuple of (httpx.Response, AsyncCodewordsResponse).
                              If False, returns the AsyncCodewordsResponse object directly.
        :param run_as_template: If True, runs the service as a template, so caller will be like owner (default: False).
        :return: httpx.Response object (body is fully read).
        """

        if in_background:
            request_id = await self.provision_request()

        path = path.lstrip("/")
        url = f"{self.base_url}/run/{service_id}/{path}"

        headers = self._auth_headers()
        headers["Content-Type"] = "application/json"
        if run_as_template:
            headers["Run-As-Template"] = "yes"
        if request_id:
            headers["X-Provisioned-Request-Id"] = request_id
        if correlation_id:
            headers["X-Correlation-Id"] = correlation_id

        task = asyncio.create_task(
            self.client.post(url, headers=headers, json=inputs, timeout=self.default_timeout)
        )
        if in_background:
            assert request_id is not None
            return AsyncCodewordsResponse(request_id, self)

        resp = await task
        resp.raise_for_status()
        return resp

    async def start_service(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        correlation_id: Optional[str] = None,
    ) -> AsyncCodewordsResponse:
        """
        Convenience method that:
          1. Provisions a request ID
          2. Runs the service with that request ID but does not wait for it to complete
          3. Returns a response object that provides access to logs and results

        :param service_id: The service to run.
        :param inputs: Payload for the service call.
        :param path: Optional path appended to /run/{service_id}.
        :param correlation_id: If provided, sends as 'X-Correlation-Id'.
        :return: AsyncCodewordsResponse object with access to logs and results
        """
        req_id = await self.provision_request()

        # Create a background task for the service call instead of waiting
        asyncio.create_task(
            self.run(service_id, path=path, request_id=req_id, inputs=inputs, correlation_id=correlation_id)
        )
        return AsyncCodewordsResponse(req_id, self)

    @asynccontextmanager
    async def stream_logs(self, request_id: str) -> AsyncGenerator[dict, None]:
        """
        GET /logs/{request_id} as NDJSON. Returns an async context manager that yields a generator of log lines.

        Usage:
            async with client.stream_logs("some-request-id") as logs:
                async for log_line in logs:
                    print(log_line)

        IMPORTANT: Must be used with 'async with', not regular 'with'

        Note: Automatically reconnects when connection times out (e.g., after App Runner's 120-second limit)
        """

        # Add __enter__ to provide a helpful error message if someone uses 'with' instead of 'async with'
        def __enter__():
            raise TypeError(
                "AsyncCodewordsClient.stream_logs is an async context manager. "
                "Use 'async with' instead of 'with'."
            )

        # Add the __enter__ method to self
        self.stream_logs.__enter__ = __enter__
        async for log in self.get_logs(request_id):
            yield log

    async def get_request_details(self, request_id: str) -> dict:
        """GET /request/{request_id} - returns the request record including request/response, times, cost, etc."""
        url = f"{self.base_url}/request/{request_id}"
        r = await self.client.get(url, headers=self._auth_headers())
        r.raise_for_status()
        return r.json()

    async def poll_result(self, request_id: str, timeout_seconds: int = 300) -> httpx.Response:
        """
        GET /result/{request_id}?timeout=X to long-poll for the request to complete.

        Because App Runner has a 2-minute timeout, this method will automatically retry
        on timeouts until the overall timeout_seconds is reached.

        :param request_id: The request ID to poll for results
        :param timeout_seconds: Maximum total time to wait for the result in seconds
        :return: The request record (includes 'responseJson' if any).
        :raises httpx.HTTPError if request finally times out or fails with non-2xx.
        """
        url = f"{self.base_url}/result/{request_id}"
        headers = self._auth_headers()
        headers["Content-Type"] = "application/json"

        # Set a reasonable individual poll timeout (App Runner limits to ~120s)
        poll_timeout = min(timeout_seconds, 110)

        start_time = asyncio.get_event_loop().time()
        deadline = start_time + timeout_seconds
        retry_count = 0
        retry_delay = 1.0
        max_retry_delay = 5.0

        while True:
            # Check if we've exceeded our overall timeout
            current_time = asyncio.get_event_loop().time()
            if current_time >= deadline:
                raise httpx.TimeoutException(f"Polling timed out after {timeout_seconds} seconds")

            # Calculate remaining time for this attempt
            remaining_time = deadline - current_time
            this_poll_timeout = min(poll_timeout, remaining_time)

            # Set params with the current poll timeout
            params = {"timeout": str(int(this_poll_timeout))}

            try:
                r = await self.client.get(url, headers=headers, params=params, timeout=None)
                r.raise_for_status()
                return r
            except (httpx.TimeoutException, httpx.ReadTimeout):
                # Expected when App Runner times out
                retry_count += 1
                await asyncio.sleep(retry_delay)
                # Exponential backoff with jitter
                retry_delay = min(
                    max_retry_delay, retry_delay * 1.5 * (0.9 + 0.2 * asyncio.get_event_loop().time() % 1)
                )
                continue
            except httpx.HTTPStatusError as e:
                # Retry on 504 Gateway Timeout or 408 Request Timeout
                if e.response.status_code in [504, 408]:
                    retry_count += 1
                    await asyncio.sleep(retry_delay)
                    # Exponential backoff with jitter
                    retry_delay = min(
                        max_retry_delay,
                        retry_delay * 1.5 * (0.9 + 0.2 * asyncio.get_event_loop().time() % 1),
                    )
                    continue
                # For other HTTP errors, raise immediately
                raise

    async def create_file_upload(self, filename: str) -> dict:
        """
        POST /file?filename=... => Returns {"upload_uri":..., "download_uri":...}.
        """
        url = f"{self.base_url}/file"
        params = {"filename": filename}
        r = await self.client.post(url, headers=self._auth_headers(), params=params)
        r.raise_for_status()
        return r.json()

    async def upload_file_content(self, filename: str, file_content: bytes) -> str:
        """
        Convenience method that:
        1. Gets upload and download URIs from create_file_upload
        2. Uploads the file to the upload URI
        3. Returns the download URL

        :param filename: Name of the file to upload
        :param file_content: Content of the file as bytes
        :return: The download URL for the uploaded file
        """
        # Get upload and download URIs
        upload_info = await self.create_file_upload(filename)
        upload_uri = upload_info["upload_uri"]
        download_uri = upload_info["download_uri"]

        # Upload the file to the provided URI
        async with httpx.AsyncClient() as client:
            response = await client.put(
                upload_uri,
                content=file_content,
                headers={"Content-Type": "application/octet-stream", "x-amz-acl": "public-read"},
            )
            response.raise_for_status()

        return download_uri

    async def upload_file(self, file_path: str, filename: str | None = None) -> str:
        """
        Convenience method that takes a file path, extracts the filename,
        reads the file content, and uploads it.

        :param file_path: Path to the file to upload
        :param filename: Optional filename to use for the uploaded file
        :return: The download URL for the uploaded file
        """
        # Extract the filename from the path
        filename = filename or os.path.basename(file_path)

        # Read the file content
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Upload the file
        return await self.upload_file_content(filename, file_content)

    async def get_logs(self, request_id: str) -> AsyncGenerator[dict, None]:
        """
        A simpler version of stream_logs that doesn't require using a context manager.
        Returns an async generator of log lines that can be iterated with 'async for'.

        Usage:
            async for log_line in client.get_logs(request_id):
                print(log_line)

        Note: Automatically reconnects when connection times out (e.g., after App Runner's 120-second limit)
        """
        headers = self._auth_headers()
        headers["Accept"] = "text/event-stream"
        headers["Content-Type"] = "application/json"
        url = f"{self.base_url}/logs/{request_id}"

        # To track the last log timestamp to avoid duplicates after reconnecting
        last_log_time = None
        max_retries = 100  # Protect against infinite retries
        retry_count = 0
        retry_delay = 1.0  # Start with 1 second delay
        max_retry_delay = 5.0  # Maximum retry delay

        while retry_count < max_retries:
            try:
                # Include last timestamp in query params if available
                params = {}
                if last_log_time:
                    params["after"] = (
                        last_log_time.isoformat() if hasattr(last_log_time, "isoformat") else last_log_time
                    )

                async with self.client.stream(
                    "GET", url, headers=headers, params=params, timeout=None
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        line_str = line.strip()
                        if not line_str:
                            continue
                        try:
                            log_entry = json.loads(line_str)

                            # Client-side filtering: Skip logs with timestamps before our last_log_time
                            if last_log_time and "createdAt" in log_entry:
                                log_time = log_entry["createdAt"]
                                # Convert string to datetime if needed for comparison
                                if isinstance(log_time, str) and isinstance(last_log_time, datetime):
                                    try:
                                        log_time = datetime.fromisoformat(log_time.replace("Z", "+00:00"))
                                    except ValueError:
                                        # If conversion fails, use string comparison as fallback
                                        if log_time <= last_log_time:
                                            continue
                                # String comparison or datetime comparison
                                elif log_time <= last_log_time:
                                    continue

                            # Update the last_log_time if available
                            if "createdAt" in log_entry:
                                last_log_time = log_entry["createdAt"]
                            yield log_entry
                        except json.JSONDecodeError:
                            yield {"rawText": line_str}

                # If we reach here, the stream ended gracefully, reset retry counter
                retry_count = 0
                retry_delay = 1.0

            except (httpx.TimeoutException, httpx.ReadTimeout) as e:
                print(e)
                # Expected exception when App Runner times out at 120 seconds
                retry_count += 1
                await asyncio.sleep(retry_delay)
                # Exponential backoff with jitter, capped at max_retry_delay
                retry_delay = min(
                    max_retry_delay, retry_delay * 1.5 * (0.9 + 0.2 * asyncio.get_event_loop().time() % 1)
                )
                continue

            except httpx.ConnectError as e:
                print(e)
                # Network connection issues
                retry_count += 1
                await asyncio.sleep(retry_delay)
                # Exponential backoff with jitter, capped at max_retry_delay
                retry_delay = min(
                    max_retry_delay, retry_delay * 1.5 * (0.9 + 0.2 * asyncio.get_event_loop().time() % 1)
                )
                continue

            except Exception as e:
                # For other exceptions, yield an error message and exit
                yield {"error": f"Log streaming error: {str(e)}"}
                break
            break


###############################################################################
#                            SYNC CODEWORDS CLIENT
###############################################################################


class CodewordsClient:
    """
    A synchronous client for interacting with the Codewords runtime server.
    It reuses a single httpx.Client for all requests in sync mode.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        default_timeout: float = 115.0,
    ):
        """
        :param base_url: Base URL of the Codewords runtime (e.g. 'https://runtime.codewords.ai').
                        If None, uses environment var `RUNTIME_URI` or fallback 'https://runtime.codewords.ai'.
        :param api_key: Your Codewords API key. If None, uses env var `CODEWORDS_API_KEY`.
        :param default_timeout: Default request timeout in seconds.
        """
        if base_url is None:
            base_url = os.getenv("RUNTIME_URI", "https://runtime.codewords.ai")

        if api_key is None:
            env_key = os.getenv("CODEWORDS_API_KEY")
            if not env_key:
                raise ValueError("CODEWORDS_API_KEY is not set")
            api_key = env_key

        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.default_timeout = default_timeout

        # Reuse a single httpx.Client (synchronous).
        self.client = httpx.Client(timeout=self.default_timeout)

    def close(self) -> None:
        """Close the underlying sync HTTP client."""
        self.client.close()

    def _auth_headers(self) -> Dict[str, str]:
        return {"Authorization": self.api_key}

    def provision_request(self) -> str:
        """Sync version: POST /provision-request."""
        url = f"{self.base_url}/provision-request"
        headers = self._auth_headers()
        headers["Content-Type"] = "application/json"
        r = self.client.post(url, headers=headers)
        r.raise_for_status()
        return r.json()["request_id"]

    @overload
    def run(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        in_background: Literal[False] = False,
    ) -> httpx.Response: ...

    @overload
    def run(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        in_background: Literal[True] = True,
        run_as_template: Optional[bool] = False,
    ) -> CodewordsResponse: ...

    def run(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        request_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        in_background: bool = False,
        run_as_template: Optional[bool] = False,
    ) -> Union[httpx.Response, CodewordsResponse]:
        """
        Synchronous POST /run/{service_id}/{path}, optionally with a pre-provisioned request_id.

        :param service_id: Target service ID.
        :param path: Optional path appended after service_id (e.g. 'predict' => /run/{service_id}/predict).
        :param request_id: If provided, sends as 'X-Provisioned-Request-Id'.
        :param correlation_id: If provided, sends as 'X-Correlation-Id'.
        :param inputs: Payload sent in the POST body. If dict, sent as JSON; str => text; bytes => raw.
        :param in_background: If True, returns a tuple of (httpx.Response, CodewordsResponse).
                              If False, returns the CodewordsResponse object directly.
        :param run_as_template: If True, runs the service as a template, so caller will be like owner (default: False).
        :return: httpx.Response object (body is fully read).
        """
        path = path.lstrip("/")
        url = f"{self.base_url}/run/{service_id}/{path}"

        if in_background:
            request_id = self.provision_request()

        headers = self._auth_headers()
        headers["Content-Type"] = "application/json"
        if request_id:
            headers["X-Provisioned-Request-Id"] = request_id
        if correlation_id:
            headers["X-Correlation-Id"] = correlation_id

        if run_as_template:
            headers["Run-As-Template"] = "yes"

        if in_background:
            assert request_id is not None
            # Instead of using asyncio, directly spawn a thread for the HTTP request
            import threading

            thread = threading.Thread(
                target=lambda: self.client.post(
                    url, headers=headers, json=inputs, timeout=self.default_timeout
                ),
                daemon=True,  # Make thread a daemon so it doesn't block program exit
            )
            thread.start()
            return CodewordsResponse(request_id, self)

        r = self.client.post(url, headers=headers, json=inputs, timeout=self.default_timeout)
        r.raise_for_status()
        return r

    def start_service(
        self,
        service_id: str,
        inputs: Optional[Union[Dict[str, Any], str, bytes]] = None,
        path: str = "",
        correlation_id: Optional[str] = None,
    ) -> CodewordsResponse:
        """
        Convenience sync method that:
          1. Provisions a request ID
          2. Runs the service with that request ID but does not wait for it to complete
          3. Returns a response object that provides access to logs and results

        :param service_id: The service to run.
        :param inputs: Payload for the service call.
        :param path: Optional path appended to /run/{service_id}.
        :param correlation_id: If provided, sends as 'X-Correlation-Id'.
        :return: CodewordsResponse object with access to logs and results
        """
        req_id = self.provision_request()
        # Create a background task for the service call instead of waiting
        # Get event loop if available, otherwise use default
        loop = asyncio.get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.create_task(
            # We need to wrap the run_service call in a coroutine
            asyncio.to_thread(
                self.run,
                service_id,
                path=path,
                request_id=req_id,
                inputs=inputs,
                correlation_id=correlation_id,
            )
        )
        return CodewordsResponse(req_id, self)

    @contextmanager
    def stream_logs(self, request_id: str) -> Generator[dict, None, None]:
        """
        GET /logs/{request_id} as NDJSON (sync).
        Returns a context manager you can use in a `with` statement:

            with client.stream_logs("some-request-id") as logs:
                for log_line in logs:
                    print(log_line)

        IMPORTANT: This is a sync context manager. If using AsyncCodewordsClient,
        use async_client.stream_logs() with 'async with' instead.

        Note: Automatically reconnects when connection times out (e.g., after App Runner's 120-second limit)
        """
        yield from self.get_logs(request_id)

    def get_logs(self, request_id: str) -> Generator[dict, None, None]:
        """
        A simpler version of stream_logs that doesn't require using a context manager.
        Returns a generator of log lines that can be iterated with 'for'.

        Usage:
            for log_line in client.get_logs("some-request-id"):
                print(log_line)

        Note: Automatically reconnects when connection times out (e.g., after App Runner's 120-second limit)
        """
        url = f"{self.base_url}/logs/{request_id}"
        headers = self._auth_headers()
        headers["Accept"] = "text/event-stream"
        headers["Content-Type"] = "application/json"

        # To track the last log timestamp to avoid duplicates after reconnecting
        last_log_time = None
        max_retries = 100  # Protect against infinite retries
        retry_count = 0
        retry_delay = 1.0  # Start with 1 second delay
        max_retry_delay = 5.0  # Maximum retry delay

        while retry_count < max_retries:
            try:
                # Include last timestamp in query params if available
                params = {}
                if last_log_time:
                    params["after"] = (
                        last_log_time.isoformat() if hasattr(last_log_time, "isoformat") else last_log_time
                    )

                # Create a response object that will be properly cleaned up
                with self.client.stream(
                    "GET", url, headers=headers, params=params, timeout=None
                ) as response:
                    for line in response.iter_lines():
                        line_str = line.decode("utf-8").strip() if isinstance(line, bytes) else line.strip()
                        if not line_str:
                            continue
                        try:
                            log_entry = json.loads(line_str)

                            # Client-side filtering: Skip logs with timestamps before our last_log_time
                            if last_log_time and "createdAt" in log_entry:
                                log_time = log_entry["createdAt"]
                                # Convert string to datetime if needed for comparison
                                if isinstance(log_time, str) and isinstance(last_log_time, datetime):
                                    try:
                                        log_time = datetime.fromisoformat(log_time.replace("Z", "+00:00"))
                                    except ValueError:
                                        # If conversion fails, use string comparison as fallback
                                        if log_time <= last_log_time:
                                            continue
                                # String comparison or datetime comparison
                                elif log_time <= last_log_time:
                                    continue

                            # Update the last_log_time if available
                            if "createdAt" in log_entry:
                                last_log_time = log_entry["createdAt"]
                            yield log_entry
                        except json.JSONDecodeError:
                            yield {"rawText": line_str}

                    # If we reach here, the stream ended gracefully, reset retry counter
                    retry_count = 0
                    retry_delay = 1.0

            except (httpx.TimeoutException, httpx.ReadTimeout):
                # Expected exception when App Runner times out at 120 seconds
                retry_count += 1
                time.sleep(retry_delay)
                # Exponential backoff with jitter, capped at max_retry_delay
                retry_delay = min(max_retry_delay, retry_delay * 1.5 * (0.9 + 0.2 * (time.time() % 1)))
                continue

            except httpx.ConnectError:
                # Network connection issues
                retry_count += 1
                time.sleep(retry_delay)
                # Exponential backoff with jitter, capped at max_retry_delay
                retry_delay = min(max_retry_delay, retry_delay * 1.5 * (0.9 + 0.2 * (time.time() % 1)))
                continue

            except Exception as e:
                # For other exceptions, yield an error message and exit
                yield {"error": f"Log streaming error: {str(e)}"}
                break
            break

    def get_request_details(self, request_id: str) -> dict:
        """Sync GET /request/{request_id}."""
        url = f"{self.base_url}/request/{request_id}"
        r = self.client.get(url, headers=self._auth_headers())
        r.raise_for_status()
        return r.json()

    def poll_result(self, request_id: str, timeout_seconds: int = 300) -> httpx.Response:
        """
        Sync GET /result/{request_id}?timeout=X to long-poll for the request to complete.

        Because App Runner has a 2-minute timeout, this method will automatically retry
        on timeouts until the overall timeout_seconds is reached.

        :param request_id: The request ID to poll for results
        :param timeout_seconds: Maximum total time to wait for the result in seconds
        :return: The request record (includes 'responseJson' if any).
        :raises httpx.HTTPError if request finally times out or fails with non-2xx.
        """
        url = f"{self.base_url}/result/{request_id}"
        headers = self._auth_headers()
        headers["Content-Type"] = "application/json"

        # Set a reasonable individual poll timeout (App Runner limits to ~120s)
        poll_timeout = min(timeout_seconds, 110)

        start_time = time.time()
        deadline = start_time + timeout_seconds
        retry_count = 0
        retry_delay = 1.0
        max_retry_delay = 5.0

        while True:
            # Check if we've exceeded our overall timeout
            current_time = time.time()
            if current_time >= deadline:
                raise httpx.TimeoutException(f"Polling timed out after {timeout_seconds} seconds")

            # Calculate remaining time for this attempt
            remaining_time = deadline - current_time
            this_poll_timeout = min(poll_timeout, remaining_time)

            # Set params with the current poll timeout
            params = {"timeout": str(int(this_poll_timeout))}

            try:
                r = self.client.get(url, headers=headers, params=params, timeout=None)
                r.raise_for_status()
                return r
            except (httpx.TimeoutException, httpx.ReadTimeout):
                # Expected when App Runner times out
                retry_count += 1
                time.sleep(retry_delay)
                # Exponential backoff with jitter
                retry_delay = min(max_retry_delay, retry_delay * 1.5 * (0.9 + 0.2 * (time.time() % 1)))
                continue
            except httpx.HTTPStatusError as e:
                # Retry on 504 Gateway Timeout
                if e.response.status_code == 504:
                    retry_count += 1
                    time.sleep(retry_delay)
                    # Exponential backoff with jitter
                    retry_delay = min(max_retry_delay, retry_delay * 1.5 * (0.9 + 0.2 * (time.time() % 1)))
                    continue
                # For other HTTP errors, raise immediately
                raise

    def create_file_upload(self, filename: str) -> dict:
        """
        Sync POST /file?filename=...
        """
        url = f"{self.base_url}/file"
        params = {"filename": filename}
        r = self.client.post(url, headers=self._auth_headers(), params=params)
        r.raise_for_status()
        return r.json()

    def upload_file_content(self, filename: str, file_content: bytes) -> str:
        """
        Convenience method that:
        1. Gets upload and download URIs from create_file_upload
        2. Uploads the file to the upload URI
        3. Returns the download URL

        :param filename: Name of the file to upload
        :param file_content: Content of the file as bytes
        :return: The download URL for the uploaded file
        """
        # Get upload and download URIs
        upload_info = self.create_file_upload(filename)
        upload_uri = upload_info["upload_uri"]
        download_uri = upload_info["download_uri"]

        # Upload the file to the provided URI
        with httpx.Client() as client:
            response = client.put(
                upload_uri,
                content=file_content,
                headers={"Content-Type": "application/octet-stream", "x-amz-acl": "public-read"},
            )
            response.raise_for_status()

        return download_uri

    def upload_file(self, file_path: str, filename: str | None = None) -> str:
        """
        Convenience method that takes a file path, extracts the filename,
        reads the file content, and uploads it.

        :param file_path: Path to the file to upload
        :param filename: Optional filename to use for the uploaded file
        :return: The download URL for the uploaded file
        """
        # Extract the filename from the path
        filename = filename or os.path.basename(file_path)

        # Read the file content
        with open(file_path, "rb") as f:
            file_content = f.read()

        # Upload the file
        return self.upload_file_content(filename, file_content)
