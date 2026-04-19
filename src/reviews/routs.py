from fastapi import APIRouter, status, HTTPException, Depends, dependencies
from src.books.models import Book, Review
from src.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.reviews.schema import ReviewCreate, ReviewOutput
from .service import ReviewService
from src.auth.depandancy import AccessTokenBearer, RoleChecker


review_router = APIRouter()
review_service = ReviewService( )
role_checker = RoleChecker(allowed_role=['admin', 'user'])
access_token = AccessTokenBearer()


@review_router.post("/", response_model=ReviewOutput, dependencies=[Depends(role_checker)])
async def CreateReview(review_data: ReviewCreate, token_detail: dict = Depends(access_token), session:AsyncSession = Depends(get_session)):
    user_uid = token_detail.get("user")['sub']
    return await review_service.create_review(review_data, user_uid, session)

