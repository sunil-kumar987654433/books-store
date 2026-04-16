from pydantic import BaseModel
import uuid
from datetime import datetime, date

class Book(BaseModel):
    key: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str

class BookUpdateModel(BaseModel):
    title: str | None = None
    author: str| None= None
    publisher: str| None= None
    page_count: int| None= None
    language: str| None= None