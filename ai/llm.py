import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm():

    llm = ChatOpenAI(
        model=os.getenv("MODEL_NAME"),
        temperature=0.3,
        api_key=os.getenv(
            "OPENAI_API_KEY"
        )
    )

    return llm