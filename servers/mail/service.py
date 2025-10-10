import io
import smtplib
import imaplib
import email
from email.message import EmailMessage
from email.header import decode_header
from typing import List

from base import MailService

class GmailService(MailService):
    """
    Сервис для работы с Gmail через SMTP (отправка) и IMAP (чтение).
    """

    def __init__(self, email_address: str, app_password: str):
        """
        :param email_address: Адрес Gmail (например, example@gmail.com)
        :param app_password: Пароль приложения (генерируется в аккаунте Google)
        """
        self.email_address = email_address
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.imap_server = "imap.gmail.com"
        self.smtp_port = 587

    # ---------- Отправка обычного письма ----------

    def send_email(self, to: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = self.email_address
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.email_address, self.app_password)
                smtp.send_message(msg)
            return True
        
        except Exception as e:
            return False
        

    # ---------- Отправка письма с вложениями ----------

    def send_email_with_attachments(self, to: str, subject: str, body: str, attachments: List[io.BytesIO]):
        msg = EmailMessage()
        msg["From"] = self.email_address
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        for i, file in enumerate(attachments, start=1):
            # если BytesIO не имеет имени — создаем имя по умолчанию
            filename = getattr(file, "name", f"attachment_{i}.bin")
            file.seek(0)
            msg.add_attachment(
                file.read(),
                maintype="application",
                subtype="octet-stream",
                filename=filename
            )
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
                smtp.starttls()
                smtp.login(self.email_address, self.app_password)
                smtp.send_message(msg)
              
            return True
        except Exception as e:
            return False

    # ---------- Получение писем ----------

    def recieve_emails(self, mailbox: str = "INBOX", limit: int = 5):
        """
        Возвращает последние письма (по умолчанию 5).
        """
        mail = imaplib.IMAP4_SSL(self.imap_server)
        mail.login(self.email_address, self.app_password)
        mail.select(mailbox)

        _, data = mail.search(None, "ALL")
        mail_ids = data[0].split()
        latest_ids = mail_ids[-limit:]

        messages = []
        for num in reversed(latest_ids):
            _, msg_data = mail.fetch(num, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_ = msg.get("From")
            body = ""

            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain" and part.get("Content-Disposition") is None:
                        body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                        break
            else:
                body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

            messages.append({
                "from": from_,
                "subject": subject,
                "body": body.strip()
            })

        mail.logout()
        print(f"📬 Получено {len(messages)} писем")
        return messages


# ---------- Пример использования ----------

if __name__ == "__main__":
    # ⚠️ Gmail требует пароль приложения (App Password)
    # Создаётся в https://myaccount.google.com/apppasswords

    service = GmailService("skoshkidko1@gmail.com", "apof qrki dokb mpai")

    # Отправить письмо
    service.send_email("target@example.com", "Тест", "Привет! Это тестовое письмо 😊")

    # Отправить письмо с вложениями
    file = io.BytesIO(b"Hello from attachment!")
    file.name = "test.txt"
    service.send_email_with_attachments("target@example.com", "Письмо с файлом", "Вот вложение:", [file])

    # Получить последние письма
    emails = service.recieve_emails(limit=3)
    for e in emails:
        print(f"\nОт: {e['from']}\nТема: {e['subject']}\nТекст:\n{e['body']}")
