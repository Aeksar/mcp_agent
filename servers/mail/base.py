from abc import ABC, abstractmethod
import io

class MailService(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str): ...

    @abstractmethod
    def send_email_with_attachments(self, to: str, subject: str, body: str, attachments: list[io.BytesIO]): ...

    @abstractmethod
    def recieve_emails(self): ...