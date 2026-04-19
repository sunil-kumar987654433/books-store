from fastapi import Depends, dependencies, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.auth.utils import HashingToken
from sqlalchemy import select
from src.auth.models import User
from datetime import datetime, timezone
from typing import List
from src.db.redis import token_in_blocklist, add_jti_to_blocklist
from src.auth.service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session


user_service = UserService()

class TokenBearer(HTTPBearer):
    
    def __init__(self, *, bearerFormat = None, scheme_name = None, description = None, auto_error = True):
        super().__init__(bearerFormat=bearerFormat, scheme_name=scheme_name, description=description, auto_error=auto_error)

    def verify_token_data(self, token_data: dict):
        raise NotImplementedError(
            "please override child class"
        )
    
    async def __call__(self, request: Request):
        
        try:
            cred= await super().__call__(request)
            token = cred.credentials.split(" ")[1]
            payload = HashingToken().decode_data(token)
            self.verify_token_data(token_data=payload)

            if await token_in_blocklist(payload.get("jti")):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail={
                        "error": "This token is invalid or expired.",
                        "resolution": "Please get net token."
                    }
                )

            return payload
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOKEN EXPIRED" 
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID TOKEN"
            )


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and token_data.get("refresh") is True:
            raise HTTPException(
                detail="Please provide access token",
                status_code=400
            )
   
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict)->None:

        if token_data and not token_data.get("refresh"):
            raise HTTPException(
                detail="Please provide refresh token",
                status_code=400
            )

class RoleChecker:
    def __init__(self, allowed_role: List[str]):
        self.allowed_role = allowed_role

    async def __call__(self, token: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
        user = await user_service.get_a_user_by_email(user_uid = token.get("user")['sub'], session=session)
        if user is None:
            raise HTTPException(
                detail="Invalid user",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        if user.role not in self.allowed_role:
            raise HTTPException(
                detail="Permission denied.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        return True
