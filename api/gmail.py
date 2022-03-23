from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from starlette.responses import JSONResponse

conf = ConnectionConfig(
    MAIL_USERNAME="klinikaprojekat45@gmail.com",
    MAIL_PASSWORD="cepidlaka",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
    MAIL_FROM="klinikaprojekat45@gmail.com",
    TEMPLATE_FOLDER="/home/fww1/PycharmProjects/pythonProject/clinic45/tempfiles"
)


async def send_mail():
    with open("/home/fww1/PycharmProjects/pythonProject/clinic45/temp/user_mail.txt", "r") \
            as mail_user:
        mail = mail_user.read()

    with open("/home/fww1/PycharmProjects/pythonProject/clinic45/temp/hashed_password.txt", "r") \
            as hash_user:
        hash = hash_user.read()
        link = "http://0.0.0.0:8000/docs#/forgot_password/forgot_password_forgot_password_recover_password_patch+sessionid=" + hash

    message = MessageSchema(
        subject="Forgotten password",
        recipients=[mail],
        body=link,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name='klinika_email.html')
    hash_user.close()
    mail_user.close()
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
