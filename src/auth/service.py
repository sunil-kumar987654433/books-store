import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schema import UserCreate, UserLogin
from sqlalchemy import insert, select, delete, or_
from fastapi import HTTPException, status
from src.auth.utils import UserPassword, HashingToken
from datetime  import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
ACCESS_TOKEN_EXPIRED = 15
REFRESH_TOKEN_EXPIRED = 2
class UserService:
    async def get_a_user_by_email(self, session: AsyncSession, email: str | None= None, user_uid: uuid.UUID|None = None):
        statement = select(User).where(
            or_(
                User.email == email,
                User.uid == user_uid
            )  
        )
        user = await session.execute(statement)
        return user.scalar_one_or_none()
        

    async def create_user(self, user_data: UserCreate, session: AsyncSession):
        is_user = await self.get_a_user_by_email(session = session, email = user_data.email)
        if is_user:
            raise HTTPException(
                detail="Username or email already exist",
                status_code=status.HTTP_403_FORBIDDEN
            )
        user_dict = user_data.model_dump()
        user_dict.pop("confirm_password")
        user_dict['password_hash'] = UserPassword().generate_password(user_dict.pop("password"))
        user_dict['role'] = 'user'
        user = User(**user_dict)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def create_new_access_token(self, user_uid: uuid.UUID, session: AsyncSession):
       
        user = await self.get_a_user_by_email(session=session, user_uid = user_uid)
        if user.is_active is False:
            raise HTTPException(
                detail='Inactive user',
                status_code=status.HTTP_403_FORBIDDEN
            )
        access_token_expired_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRED)
        access_token= HashingToken().encode_data(
                {
                    "user":{
                        "sub":str(user.uid),
                        "user_email": user.email,
                        'user_role': user.role,
                    },
                    "exp": access_token_expired_time,
                    "refresh": False
                }
            )
            
        if access_token_expired_time.tzinfo is None:
            access_token_expired_time = access_token_expired_time.replace(tzinfo=timezone.utc)
        access_token_expired_time = access_token_expired_time.astimezone(ZoneInfo("Asia/Kolkata")).isoformat()
        return {
                "access_token": access_token,
                "access_token_expired_time": access_token_expired_time,
                "user_uid": str(user.uid),
                "user_email": user.email
            }
        
    
    async def login_user(self, user_data: UserLogin, session: AsyncSession):
        user = await self.get_a_user_by_email(session=session, email=user_data.email)
        if user is None:
            raise HTTPException(
                detail="email not exxist",
                status_code=status.HTTP_403_FORBIDDEN
            )
        if user.is_active is False:
            raise HTTPException(
                detail="User is inactive",
                status_code=status.HTTP_403_FORBIDDEN
            )
        if UserPassword().verify_password(user_data.password, user.password_hash):
            access_token_expired_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRED)
            refresh_token_expired_time = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRED)
            access_token= HashingToken().encode_data(
                {   
                    "user":{
                        "sub":str(user.uid),
                        "user_email": user.email,
                        'user_role': user.role,
                    },
                    "exp": access_token_expired_time,
                    "refresh": False,
                }
            )
            
            if access_token_expired_time.tzinfo is None:
                access_token_expired_time = access_token_expired_time.replace(tzinfo=timezone.utc)
            access_token_expired_time = access_token_expired_time.astimezone(ZoneInfo("Asia/Kolkata")).isoformat()

            refresh_token= HashingToken().encode_data(
                {
                    "user":{
                        "sub":str(user.uid),
                        "user_email": user.email,
                        'user_role': user.role,
                    },
                    "exp": refresh_token_expired_time,
                    "refresh": True
                }
            )
            if refresh_token_expired_time.tzinfo is None:
                refresh_token_expired_time = refresh_token_expired_time.replace(tzinfo=timezone.utc)
            print("refresh_token_expired_time===", refresh_token_expired_time)
            refresh_token_detail = {
                "refresh_token": refresh_token,
                'refresh_token_expired_time': str(int((refresh_token_expired_time - datetime.now(timezone.utc) ).total_seconds()))
            }
            return {
                "access_token": access_token,
                "access_token_expired_time": access_token_expired_time,
                "refresh_token_detail": refresh_token_detail,
                "user_uid": str(user.uid),
                "user_email": user.email
            }
        raise HTTPException(
                detail="Invalid password.",
                status_code=status.HTTP_403_FORBIDDEN
            )