from sqlmodel import SQLModel, Field
from sqlalchemy import DateTime, String, Column, Integer, func, text
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import date

class Book(SQLModel, table=True):
    __tablename__ = 'books'
    # __table_args__ = {
    #     "schema": "books"
    # }

    key: uuid.UUID = Field(sa_column=Column(
        pg.UUID(as_uuid=True), nullable=False, unique=True, primary_key=True
    ), default_factory=uuid.uuid4)
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

    def __repr__(self):
        return f"<Book (title: {self.title})>"
    


