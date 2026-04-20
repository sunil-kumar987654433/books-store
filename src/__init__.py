from fastapi import FastAPI, status, Request, responses
from src.books.router import book_router
from src.auth.routes import auth_router
from src.reviews.routs import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import (
    BooklyException, InvalidTokenException, RevokedToken, AccessTokenRequired, RefreshTokenRequired, UserAlreadyExist, InsufficientPermission, BookNotFound, TagNotFound, NotFound, create_exeption_handlers, register_all_errors
)
from .middleware import register_middleware



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is start...")
    from src.books import models as book_models
    from src.auth import models as auth_models
    await init_db()
    yield
    print("server is stoped...")

version = 'v1'

app = FastAPI(
    title='bookly',
    description="A rest api for book review",
    version=version,
    # lifespan=lifespan
)
app.include_router(book_router, tags=['books'], prefix=f'/api/{version}/books')
app.include_router(auth_router, tags=['auth'], prefix=f'/api/{version}/auth')
app.include_router(review_router, tags=['review'], prefix=f'/api/{version}/review')


register_all_errors(app)
register_middleware(app)

@app.exception_handler(500)
async def internal_server_error(request:Request, exc):
    return responses.JSONResponse(
        content={
            "message": 'Ooops! something went wrong.Please wait',
            "error_code": 'server error'
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


