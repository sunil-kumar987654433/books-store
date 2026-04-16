from fastapi import FastAPI
from src.books.router import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db


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
    lifespan=lifespan
)
app.include_router(book_router, tags=['books'], prefix=f'/api/{version}/books')
app.include_router(auth_router, tags=['auth'], prefix=f'/api/{version}/auth')


