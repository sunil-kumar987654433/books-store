from fastapi import FastAPI, middleware, Request, responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import os
from datetime import datetime, timezone
import jwt
from src.config import Config
import logging
from logging.handlers import TimedRotatingFileHandler

os.makedirs("logs", exist_ok=True)

# ✅ custom logger (NOT uvicorn)
app_logger = logging.getLogger("app.audit")
app_logger.setLevel(logging.INFO)
app_logger.propagate = False
JWT_SECRET_KEY = Config.JWT_SECRET
JWT_ALGORITHAM = Config.JWT_ALGORITHM
# formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# handler (pehle banao)
handler = TimedRotatingFileHandler(
    "logs/access.log",
    when="midnight",
    interval=1,
    backupCount=0
)

handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)

# attach once
if not app_logger.handlers:
    app_logger.addHandler(handler)

def register_middleware(app: FastAPI):

    app.add_middleware(
        CORSMiddleware, 
        # allow_origins = ["*"],
        allow_origins = ["http://begining.fun", "https://begining.fun"],
        allow_methods = ["*"],
        allow_headers = ['*'],
        allow_credentials = True
        )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts = [
            "begining.fun", 
            "www.begining.fun", 
            "13.233.225.195",
            "localhost",
            "127.0.0.1"
            ]
    )

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        start_time = time.perf_counter()

        ip = request.headers.get("x-forwarded-for")
        if ip:
            ip = ip.split(",")[0]
        else:
            ip = request.client.host if request.client else "unknown"

        user_agent = request.headers.get("user-agent", "unknown")

        user = "anonymous"
        auth_header = request.headers.get("authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHAM])
                user = payload.get("sub", "unknown")
            except jwt.ExpiredSignatureError:
                user = "token_expired"
            except jwt.InvalidTokenError:
                user = "invalid_token"

        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        app_logger.info(
            f"IP: {ip} | USER: {user} | "
            f"{request.method} {request.url.path} | "
            f"STATUS: {response.status_code} | "
            f"TIME: {process_time:.4f}s | "
            f"AGENT: {user_agent}"
        )

        return response

    # @app.middleware("http")
    # async def custom_login(request: Request, call_next):
    #     start_time = time.perf_counter()
    #     response = await call_next(request)
    #     process_time = time.perf_counter()- start_time
    #     logger.info(
    #         f"{request.client.host if request.client else 'unknown'} - "
    #         f"{request.method} {request.url.path} - "
    #         f"{response.status_code} - "
    #         f"{process_time:.4f}s"
    #     )
     
    #     return response
    
    # @app.middleware("http")
    # async def authorization(request: Request, call_next):
    #     if not "Authorization" in request.headers:
    #         return responses.JSONResponse(
    #             content={
    #                 "message": "not authenticated"
    #             }
    #         )
    #     response = await call_next(request)
    #     return response

