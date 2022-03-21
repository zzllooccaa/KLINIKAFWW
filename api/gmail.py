from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from starlette.responses import JSONResponse

gmail_router = APIRouter()

with open("/home/fww1/PycharmProjects/pythonProject/clinic45/static/requirements/user_mail.txt", "r") as mail_user:
    mail = mail_user.read()

conf = ConnectionConfig(
    MAIL_USERNAME="klinikaprojekat45@gmail.com",
    MAIL_PASSWORD="cepidlaka",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    MAIL_FROM="klinikaprojekat45@gmail.com"
)


@gmail_router.post("/send_mail")
async def send_mail():
    template = """
        <html>
        <body>


<p>Dear, !!!
        <br>Your link to change password is , keep using it..!!!</p>


        </body>
        </html>
        """

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[mail],
        body=template,
        subtype="html"
    )

    print(message)
    fm = FastMail(conf)
    await fm.send_message(message)
    print(message)

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
