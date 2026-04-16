import uuid
from src.books.models import Book
from fastapi import APIRouter, status, Depends
from src.books.schema import BookCreateModel, Book as BookResponse, BookUpdateModel
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.services import BookService
from src.auth.depandancy import AccessTokenBearer

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()


@book_router.get("/", status_code=status.HTTP_200_OK, response_model=list[BookResponse])
async def get_all_books(session:AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    return await book_service.get_all_books(session)

@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookResponse)
async def create_a_book(book_data: BookCreateModel, session: AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    return await book_service.create_books(
        book_data=book_data,
        session=session
    )

@book_router.get("/{book_key}", status_code=status.HTTP_200_OK, response_model=BookResponse)
async def get_a_books(book_key: uuid.UUID, session:AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    return await book_service.get_books(
        book_key, session
    )

@book_router.patch("/{book_key}", status_code=status.HTTP_200_OK, response_model=BookResponse)
async def update_a_books(book_key: uuid.UUID,book_data: BookUpdateModel, session:AsyncSession=Depends(get_session), user_detail = Depends(access_token_bearer)):
    return await book_service.update_books(
        book_key,book_data,  session
    )

@book_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_key: uuid.UUID, session:AsyncSession=Depends(get_session), user_detail=Depends(access_token_bearer)):
    return await book_service.delete_book(book_key, session)