from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import path_temp

from starlette.responses import JSONResponse

conf = ConnectionConfig(
    MAIL_USERNAME="klinikaprojekat45@gmail.com",
    MAIL_PASSWORD="cepidlaka",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    MAIL_FROM="klinikaprojekat45@gmail.com",
)


async def send_mail(email, token):

    link = "http://0.0.0.0:8000/docs#/forgot_password/forgot_password_forgot_password_recover_password_patch" \
           "?token=" + token

    message = MessageSchema(
        subject="Forgotten password",
        recipients=[email],
        body=link,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='klinika_email.html')
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
