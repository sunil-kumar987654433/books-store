from src.books.models import Book
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
import uuid
from src.books.schema import BookCreateModel, BookUpdateModel
from sqlalchemy import func, desc, asc
from fastapi import HTTPException, status

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_books(self, book_key:uuid.UUID, session: AsyncSession):
        statement = select(Book).where(
            Book.key == book_key
        )
        result = await session.execute(statement)
        
        book = result.scalar_one_or_none()
        if book is None:
            raise HTTPException(
                detail="No record found",
                status_code=status.HTTP_404_NOT_FOUND
            )
        return book


    async def create_books(self, book_data: BookCreateModel, session: AsyncSession):
        book = Book(**(book_data.model_dump()))
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book
    
    

    async def update_books(self, book_key: uuid.UUID, book_data: BookUpdateModel, session: AsyncSession):
        book = await self.get_books(book_key, session)
        for k, v in (book_data.model_dump(exclude_unset=True)).items():
            setattr(book, k, v)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

        



    async def delete_book(self, book_key: uuid.UUID, session: AsyncSession):
        book = await self.get_books(book_key, session)
        await session.delete(book)
        await session.commit()