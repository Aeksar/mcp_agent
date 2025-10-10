from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import base64
import os
import io

from service import GmailService
from utils import convert_attachments, load_config

mcp = FastMCP("mail")

config = load_config()
service = GmailService(config.EMAIL_ADDRESS, config.APP_PASSWORD)

@mcp.tool()
def send_email(to: str, subject: str, body: str):
    """
    Отправляет письмо на указанный адрес с указанным предметом и текстом.

    :param to: Адрес получателя.
    :param subject: Предмет письма.
    :param body: Текст письма.
    """
    status = service.send_email(to, subject, body)
    if status:
        return {"message": f"Email sent to {subject}"}
    return {"message": f"Failed to send email to {subject}"}


@mcp.tool()
def send_email_with_attachments(to: str, subject: str, body: str, attachments: list[str]):
    """
    Отправляет письмо с вложениями на указанный адрес с указанным предметом и текстом.

    :param to: Адрес получателя.
    :param subject: Предмет письма.
    :param body: Текст письма.
    :param attachments: Список вложений в формате base64.
    """
    files = convert_attachments(attachments)
    status = service.send_email_with_attachments(to, subject, body, files)
    if status:
        return {"message": f"Email sent to {subject}"}
    return {"message": f"Failed to send email to {subject}"}


@mcp.tool()
def recieve_emails(mailbox: str = "INBOX", limit: int = 5):
    """
    Возвращает последние письма (по умолчанию 5) из указанного ящика.

    :param mailbox: Имя ящика (по умолчанию "INBOX").
    :param limit: Количество писем (по умолчанию 5).
    :return: Список словарей с информацией о письмах.
    """
    emails = service.recieve_emails(mailbox, limit)
    return {"emails": emails}



if __name__ == "__main__":
    mcp.run(transport="stdio")