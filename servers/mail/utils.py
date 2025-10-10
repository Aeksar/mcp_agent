from dataclasses import dataclass
import base64
import io
import json


@dataclass
class Config:
    EMAIL_ADDRESS: str
    APP_PASSWORD: str

def convert_attachments(attachments: list[str]) -> list[io.BytesIO]:
    files = []
    for i, b64_data in enumerate(attachments, start=1):
        try:
            binary_data = base64.b64decode(b64_data)
            buf = io.BytesIO(binary_data)
            buf.name = f"attachment_{i}.bin"
            files.append(buf)
        except Exception as e:
            return {"error": f"Ошибка при декодировании вложения {i}: {str(e)}"}
        

def load_config(path: str = "credentials.json"):
    with open(path, "r") as f:
        data = json.load(f)
    return Config(**data)
