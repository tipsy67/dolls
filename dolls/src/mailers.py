import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from config import settings


def sendmail_cmd(recipients_emails: list, title: str, content: str):
    """
    Функция отправки писем
    """
    text_content = strip_tags(content)

    msg = EmailMultiAlternatives(
        subject=title,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=recipients_emails,)

    msg.attach_alternative(content, "text/html")
    # Добавляем заголовки для правильного отображения
    msg.mixed_subtype = 'related'
    msg.encoding = 'utf-8'
    msg.content_subtype = 'html'

    try:
        msg.send()
    except smtplib.SMTPException:
        print("Error: unable to send email")




