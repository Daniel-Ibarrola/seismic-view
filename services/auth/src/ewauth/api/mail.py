from flask import render_template
from flask_mail import Message
from typing import Union

from ewauth import CONFIG, mail


def send_email(
        to: str,
        subject: str,
        html_template: str,
        text_template: str,
) -> None:
    msg = Message(
        subject=subject,
        recipients=[to],
        sender=CONFIG.MAIL_USERNAME,
        body=text_template,
        html=html_template
    )
    mail.send(msg)


def send_confirmation_email(email: str, token: Union[bytes, str]) -> None:
    url = f"{CONFIG.DOMAIN_NAME}/confirm/{token}"
    html_template = render_template("confirm.html", url=url)
    text_template = render_template("confirm.txt", url=url)
    send_email(
        email,
        "Confirme su cuenta",
        html_template=html_template,
        text_template=text_template,
    )


def send_reset_password_email(email: str, token: Union[bytes, str]) -> None:
    url = f"{CONFIG.DOMAIN_NAME}/reset/{token}"
    html_template = render_template("reset.html", url=url, token=token)
    text_template = render_template("reset.txt", url=url, token=token)
    send_email(
        email,
        "Recupere su password",
        html_template=html_template,
        text_template=text_template,
    )
