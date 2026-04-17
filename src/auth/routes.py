from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.auth.service import UserService
from src.auth.schema import UserCreate, UserLogin
from src.auth.depandancy import RefreshTokenBearer



auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/signup")
async def CreateUserAccount(user_data: UserCreate, session: AsyncSession= Depends(get_session)):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            detail="both password must be same",
            status_code=404
        )
    return await user_service.create_user(user_data, session)


@auth_router.post("/signin")
async def UserSignInAccount(user_data: UserLogin, session: AsyncSession= Depends(get_session)):
    result =  await user_service.login_user(user_data, session)
    res = result.pop("refresh_token_detail")
    response = JSONResponse(
        content=result
    )
    response.set_cookie(
        key='refresh',
        value=res.get("refresh_token"),
        max_age=res.get("refresh_token_expired_time") ,
        secure=True, 
        httponly=True,
    )
    return response

@auth_router.get("/refresh-token")
async def get_new_access_token(token_detail:dict = Depends(RefreshTokenBearer()), session: AsyncSession = Depends(get_session)):
    user_uid = token_detail.get("sub")
    return await user_service.create_new_access_token(user_uid, session)
    