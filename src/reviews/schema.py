from datetime import datetime

from sqlmodel import SQLModel
import uuid

class ReviewCreate(SQLModel):
    book_uid: uuid.UUID
    review_text: str
    ratting: int

class ReviewOutput(SQLModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    book_uid: uuid.UUID
    review_text: str
    ratting: int
    created_at: datetime
    updated_at: datetime

