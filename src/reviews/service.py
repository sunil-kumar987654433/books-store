from fastapi import APIRouter, status, HTTPException, Depends, dependencies
from src.books.models import Book, Review
from src.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.reviews.schema import ReviewCreate
import uuid
from sqlalchemy.exc import IntegrityError
import logging
class ReviewService:


    async def create_review(self, review_data: ReviewCreate, user_uid: uuid.UUID, session:AsyncSession):
        try:
            review = Review(**(review_data.model_dump()), user_uid=user_uid)
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review
        except IntegrityError as e:
            logging.exception(str(e))
            raise HTTPException(
                detail=f"user or book are wrong",
                status_code=status.HTTP_403_FORBIDDEN
            )
        except Exception as e:
            logging.exception(str(e))
            raise HTTPException(
                detail=f"error2--- ",
                status_code=status.HTTP_403_FORBIDDEN
            )
