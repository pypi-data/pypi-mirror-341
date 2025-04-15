import json
import threading
import time
import traceback
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from logging import Logger
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Sequence
from maleo_core.models.base.schemas.responses.general import BaseGeneralResponsesSchemas

class BaseMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        logger:Logger,
        allow_origins:Sequence[str] = (),
        allow_methods:Sequence[str] = ("GET",),
        allow_headers:Sequence[str] = (),
        allow_credentials:bool = False,
        limit:int = 10,
        window:int = 1,
        cleanup_interval:int = 60,
        ip_timeout: int = 300
    ):
        super().__init__(app)
        self.logger = logger
        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = allow_headers
        self.allow_credentials = allow_credentials
        self.limit = limit
        self.window = timedelta(seconds=window)
        self.cleanup_interval = timedelta(seconds=cleanup_interval)
        self.ip_timeout = timedelta(seconds=ip_timeout)
        self.requests:dict[str, list[datetime]] = defaultdict(list)
        self.last_seen: dict[str, datetime] = {}
        self.last_cleanup = datetime.now()
        self._lock = threading.RLock()  #* Use RLock for thread safety

    def _cleanup_old_data(self) -> None:
        """
        Periodically clean up old request data to prevent memory growth.
        Removes:
        1. IPs with empty request lists
        2. IPs that haven't been seen in ip_timeout period
        """
        now = datetime.now()
        if now - self.last_cleanup > self.cleanup_interval:
            with self._lock:
                #* Remove inactive IPs (not seen recently) and empty lists
                inactive_ips = []
                for ip in list(self.requests.keys()):
                    #* Remove IPs with empty timestamp lists
                    if not self.requests[ip]:
                        inactive_ips.append(ip)
                        continue
                        
                    #* Remove IPs that haven't been active recently
                    last_active = self.last_seen.get(ip, datetime.min)
                    if now - last_active > self.ip_timeout:
                        inactive_ips.append(ip)
                
                #* Remove the inactive IPs
                for ip in inactive_ips:
                    if ip in self.requests:
                        del self.requests[ip]
                    if ip in self.last_seen:
                        del self.last_seen[ip]
                
                # Update last cleanup time
                self.last_cleanup = now
                self.logger.debug(f"Cleaned up request cache. Removed {len(inactive_ips)} inactive IPs. Current tracked IPs: {len(self.requests)}")

    def _extract_client_ip(self, request:Request) -> str:
        """Extract client IP with more robust handling of proxies"""
        #* Check for X-Forwarded-For header (common when behind proxy/load balancer)
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            #* The client's IP is the first one in the list
            ips = [ip.strip() for ip in x_forwarded_for.split(",")]
            return ips[0]
        
        #* Check for X-Real-IP header (used by some proxies)
        x_real_ip = request.headers.get("X-Real-IP")
        if x_real_ip:
            return x_real_ip
            
        #* Fall back to direct client connection
        return request.client.host if request.client else "unknown"

    def _check_rate_limit(self, client_ip:str) -> bool:
        """Check if the client has exceeded their rate limit"""
        with self._lock:
            now = datetime.now() #* Define current timestamp
            self.last_seen[client_ip] = now #* Update last seen timestamp for this IP

            #* Filter requests within the window
            self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if now - timestamp <= self.window]

            #* Check if the request count exceeds the limit
            if len(self.requests[client_ip]) >= self.limit:
                return True

            #* Add the current request timestamp
            self.requests[client_ip].append(now)
            return False

    def _append_cors_headers(self, request:Request, response:Response) -> Response:
        origin = request.headers.get("Origin")

        if origin in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allow_methods)
            response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allow_headers)
            response.headers["Access-Control-Allow-Credentials"] = "true" if self.allow_credentials else "false"

        return response

    def _add_response_headers(self, request:Request, response:Response, request_timestamp:datetime, process_time:int) -> Response:
        #* Add or update Process Time Header
        response.headers["X-Process-Time"] = str(process_time)

        #* Add request timestamp header
        response.headers["X-Request-Timestamp"] = request_timestamp.isoformat()

        #* Add response timestamp header
        response.headers["X-Response-Timestamp"] = datetime.now(tz=timezone.utc).isoformat()

        #* Re-append CORS headers
        response = self._append_cors_headers(request=request, response=response)

        return response

    async def dispatch(self, request:Request, call_next):
        self._cleanup_old_data() #* Run periodic cleanup
        request_timestamp = datetime.now(tz=timezone.utc) #* Record the request timestamp
        start_time = time.perf_counter() #* Record the start time
        client_ip = self._extract_client_ip(request) #* Get request IP with improved extraction

        #* Check rate limit
        is_rate_limit_exceeded = self._check_rate_limit(client_ip=client_ip)
        if is_rate_limit_exceeded:
            process_time = time.perf_counter() - start_time #* Calculate the process time
            response = JSONResponse(content=BaseGeneralResponsesSchemas.RateLimitExceeded().model_dump(), status_code=status.HTTP_429_TOO_MANY_REQUESTS)

            #* Add headers
            response = self._add_response_headers(request=request, response=response, request_timestamp=request_timestamp, process_time=process_time)

            #* Log Request
            self.logger.warning(f"Request | IP: {client_ip} | Method: {request.method} | Base URL: {request.base_url} | URL Path: {request.url.path} | Headers: {request.headers.items()} - Response | Status: {is_rate_limit_exceeded.status_code}")

            return response #* Return response

        #* Try to get Response to catch exception
        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time #* Calculate the process time

            #* Add headers
            response = self._add_response_headers(request=request, response=response, request_timestamp=request_timestamp, process_time=process_time)

            #* Log Request
            self.logger.info(f"Request | IP: {client_ip} | Method: {request.method} | Base URL: {request.base_url} | URL Path: {request.url.path} | Path Params: {request.path_params} | Query Params: {request.query_params} | Headers: {request.headers.items()} - Response | Status: {response.status_code} | Headers: {response.headers.items()}")

            return response #* Return response

        except Exception as e:
            process_time = time.perf_counter() - start_time #* Calculate the process time
            error_details = {
                "error": str(e),
                "traceback": traceback.format_exc().split("\n"),  #* Get full traceback
                "client_ip": client_ip,
                "method": request.method,
                "url": request.url.path,
                "headers": dict(request.headers),
            }
            response = JSONResponse(content=BaseGeneralResponsesSchemas.ServerError().model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

            #* Add headers
            response = self._add_response_headers(request=request, response=response, request_timestamp=request_timestamp, process_time=process_time)

            #* Log Request
            self.logger.error(f"Request | IP: {client_ip} | Method: {request.method} | Base URL: {request.base_url} | URL Path: {request.url.path} | Headers: {request.headers.items()} - Response | Status: {response.status_code} | Exception:\n{json.dumps(error_details, indent=4)}")

            return response #* Return response

def add_base_middleware(
    app:FastAPI,
    logger:Logger,
    allow_origins:Sequence[str] = (),
    allow_methods:Sequence[str] = ("GET",),
    allow_headers:Sequence[str] = (),
    allow_credentials:bool = False,
    limit:int = 10,
    window:int = 1,
    cleanup_interval:int = 60,
    ip_timeout:int = 300
) -> None:
    """
    Adds Base middleware to the FastAPI application.

    Args:
        app: FastAPI
            The FastAPI application instance to which the middleware will be added.

        logger: Logger
            The middleware logger to be used.

        limit: int
            Request count limit in a specific window of time

        window: int
            Time window for rate limiting (in seconds).

        cleanup_interval: int
            How often to clean up old IP data (in seconds).

        ip_timeout: int
            How long to keep an IP in memory after its last activity (in seconds).
            Default is 300 seconds (5 minutes).

    Returns:
        None: The function modifies the FastAPI app by adding Base middleware.

    Note:
        FastAPI applies middleware in reverse order of registration, so this middleware
        will execute after any middleware added subsequently.

    Example:
    ```python
    add_base_middleware(app=app, limit=10, window=1, cleanup_interval=60, ip_timeout=300)
    ```
    """
    app.add_middleware(
        BaseMiddleware,
        logger=logger,
        allow_origins=allow_origins,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        allow_credentials=allow_credentials,
        limit=limit,
        window=window,
        cleanup_interval=cleanup_interval,
        ip_timeout=ip_timeout
    )