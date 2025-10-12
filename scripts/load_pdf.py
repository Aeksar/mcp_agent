from langchain_community.document_loaders import PyPDFLoader
import os

from app.configs.settings import settings
from app.vectordb.store import get_store, load_to_store


def load_pdf_to_store(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    store = get_store(settings.collection_name)
    contents = [doc.page_content for doc in docs]
    load_to_store(store, contents)


def main():
    pdf_path = input("Введите абсолютный путь до pdf файла: ")
    if not os.path.exists(pdf_path):
        print("Файл не найден. Проверьте путь")
        return
    load_pdf_to_store(pdf_path)
    print("Загрузка завершена")


if __name__ == "__main__":
    main()