from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3
    )

    return llm