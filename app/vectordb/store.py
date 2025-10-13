from qdrant_client import QdrantClient, models
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.vectorstores.base import VectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from uuid import uuid4

from app.configs.settings import settings


def get_store(collection_name: str) -> VectorStore:
    qdrant = QdrantClient(url=settings.qdrant_url)
    embeddings = HuggingFaceEmbeddings(model_name=settings.embeddings_model)
    if not qdrant.collection_exists(collection_name):
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config={
                "size": 768,
                "distance": models.Distance.COSINE
            }
    )
    return QdrantVectorStore(
        client=qdrant,
        embedding=embeddings,
        collection_name=collection_name
    )


def load_to_store(vectorstore: VectorStore, contents: list[str]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,
        separators=["\n\n", "\n", "."]
    )
    texts = []
    metadatas = []
    ids = []

    for content in contents:
        chunks = splitter.split_text(content)
        for j, chunk in enumerate(chunks):
            texts.append(chunk)
            metadatas.append({"chunk": j})
            ids.append(uuid4().hex)
    vectorstore.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids,
    )
