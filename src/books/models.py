from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime, String, Column, Integer, func, text
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import date
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import  User

class Book(SQLModel, table=True):
    __tablename__ = 'books'
    key: uuid.UUID = Field(sa_column=Column(
        pg.UUID(as_uuid=True), nullable=False, unique=True, primary_key=True
    ), default_factory=uuid.uuid4)
    user_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key='auth_users.uid',
    )
    title: str = Field(
        description='Name of the books', index=True)
        
    author: str = Field(
        description="Author name of books", index=True)
    
    publisher: str = Field(
         description="Publisher name of books")
    published_date: date = Field(
        sa_column=Column(
            pg.DATE
        ),
        description="The date the book was published"
    )
    
    page_count: int = Field( description="Page in books")
    language: str = Field( description="Language of books", index=True)
    created_at: datetime = Field(
            sa_column=Column(
                pg.TIMESTAMP(timezone=True),
                # server_default=text("TIMEZONE('utc', 'now')"),
                default=lambda: datetime.now(timezone.utc)
            )
        )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            # default=text("TIMEZONE('utc', 'now')"),
            default=lambda: datetime.now(timezone.utc),
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )

    user: Optional['User'] = Relationship(back_populates="books")
    reviews: List['Review']  =Relationship(back_populates='book', sa_relationship_kwargs={"lazy":"selectin"})


    def __repr__(self):
        return f"<Book (title: {self.title})>"
    


class Review(SQLModel, table=True):
    __tablename__ = 'reviews'

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            unique=True,
            primary_key=True,
            nullable=False
        ), default_factory=uuid.uuid4
    )
    user_uid: uuid.UUID = Field(
        foreign_key="auth_users.uid",
        index=True
    )
    book_uid: uuid.UUID = Field(
        foreign_key="books.key", index=True
    )
    review_text: str
    ratting: int = Field(default=5, ge=1, le=5)
    created_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    ))
    updated_at: datetime = Field(sa_column=Column(
        pg.TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    ))
    user: "User" = Relationship(back_populates='reviews')
    book: "Book" = Relationship(back_populates='reviews')

    def __repr__(self):
        return f'<Review (user: {self.user_uid})>'
