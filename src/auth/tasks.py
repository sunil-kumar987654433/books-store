
from src.celery import c_app
from src.mail import SendMessage
from asgiref.sync import async_to_sync

@c_app.task()
def send_email(reciepients: list[str], subject: str, html_message: str):
    data = {
        "reciepients": reciepients,
        "subject": subject,
        "html_message": html_message
    }
    
    async_to_sync(SendMessage)(data)