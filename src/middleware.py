from fastapi import FastAPI, middleware, Request, responses
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

import time
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("uvicorn.access")

# logger.disabled = True

def register_middleware(app: FastAPI):

    app.add_middleware(
        CORSMiddleware, 
        allow_origins = ["*"],
        allow_methods = ["*"],
        allow_headers = ['*'],
        allow_credentials = True
        )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts = ["localhost", "127.0.0.1", 'https://books-store-22p9.onrender.com/']
    )
    

    @app.middleware("http")
    async def custom_login(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter()- start_time
        logger.info(
            f"{request.client.host} - "
            f"{request.method} {request.url.path} - "
            f"{response.status_code} - "
            f"{process_time:.4f}s"
        )
     
        return response
    
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

