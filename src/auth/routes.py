from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_session
from src.auth.service import UserService
from src.auth.schema import UserCreate, UserLogin, UserModel, UserBookModel
from src.auth.depandancy import RefreshTokenBearer, AccessTokenBearer, RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.mail import SendMessage
from src.auth.tasks import send_email

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_role=['admin', "user"])

@auth_router.post("/signup", response_model=UserModel)
async def CreateUserAccount(user_data: UserCreate, bg_task: BackgroundTasks, session: AsyncSession= Depends(get_session)):
    if user_data.password != user_data.confirm_password:
        raise HTTPException(
            detail="both password must be same",
            status_code=404
        )

    user =  await user_service.create_user(user_data, session)
    html_message = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                <!DOCTYPE html>

<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Welcome</title>
</head>
<body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">

  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f8; padding:20px 0;">
    <tr>
      <td align="center">

```
    <!-- Main Container -->
    <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:10px; overflow:hidden; box-shadow:0 4px 12px rgba(0,0,0,0.1);">

      <!-- Header -->
      <tr>
        <td style="background:#4f46e5; color:#ffffff; padding:20px; text-align:center;">
          <h1 style="margin:0; font-size:24px;">🚀 Welcome!</h1>
        </td>
      </tr>

      <!-- Body -->
      <tr>
        <td style="padding:30px; color:#333333;">
          <h2 style="margin-top:0;">Hey there 👋</h2>
          <p style="line-height:1.6;">
            Thanks for signing up! We're excited to have you onboard.
          </p>

          <p style="line-height:1.6;">
            You can now explore all features and start building amazing things with us.
          </p>

          <!-- Button -->
          <div style="text-align:center; margin:30px 0;">
            <a href="#" style="background:#4f46e5; color:#ffffff; padding:12px 24px; text-decoration:none; border-radius:6px; display:inline-block; font-weight:bold;">
              Get Started
            </a>
          </div>

          <p style="font-size:14px; color:#666;">
            If you have any questions, feel free to reply to this email—we're here to help.
          </p>
        </td>
      </tr>

      <!-- Footer -->
      <tr>
        <td style="background:#f4f6f8; text-align:center; padding:20px; font-size:12px; color:#888;">
          © 2026 Your Company. All rights reserved.
        </td>
      </tr>

    </table>

  </td>
</tr>
```

  </table>

</body>
</html>

            </body>
            </html>
        """
    if user:
        send_email.delay(reciepients=[user.email], subject='verify email', html_message=html_message)
        return user


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
    user_uid = token_detail.get("user").get("sub")
    return await user_service.create_new_access_token(user_uid, session)


@auth_router.get("/logout")
async def revook_token(token_detail: dict = Depends(AccessTokenBearer())):
    jti = token_detail['jti']
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logout Succesfully."
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.get("/me", response_model=UserBookModel)
async def get_current_user(user = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session), _: bool = Depends(role_checker)):
    return await user_service.get_a_user_by_email(user_uid=user.get("user").get("sub"), session=session)
