from fastapi.responses import JSONResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from src.config import Config
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    MAIL_USERNAME = Config.MAIL_USERNAME,
    MAIL_PASSWORD = Config.MAIL_PASSWORD,
    MAIL_FROM = Config.MAIL_FROM,
    MAIL_PORT = Config.MAIL_PORT,
    MAIL_SERVER = Config.MAIL_SERVER,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER=Path(BASE_DIR, 'templates')
)

mail = FastMail(
    config=mail_config
    )




async def SendMessage(data):
    message = MessageSchema(
        subject=data.get("subject"),
        recipients=data.get("reciepients"),
        body=data.get("html_message"),
        subtype=MessageType.html
        )

    result = await mail.send_message(message)
    print("result====", result)