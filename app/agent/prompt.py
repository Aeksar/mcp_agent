from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

from datetime import datetime

user_prompt = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {input}
Answer:
"""

tamplate = ChatPromptTemplate.from_messages([
    ("system", f"Current_time: {datetime.now()}"),
    MessagesPlaceholder("history"),
    ("human", user_prompt),
    MessagesPlaceholder("agent_scratchpad"),
])

