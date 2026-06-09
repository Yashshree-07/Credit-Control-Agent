# import os

# from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI

# from langchain.schema import HumanMessage


# load_dotenv()


# class LLMService:

#     def __init__(self):

#         self.llm = ChatOpenAI(

#             model="gpt-4o-mini",

#             temperature=0.7,

#             api_key=os.getenv(
#                 "OPENAI_API_KEY"
#             )
#         )

#     def generate(
#         self,
#         prompt
#     ):

#         response = self.llm.invoke([

#             HumanMessage(
#                 content=prompt
#             )
#         ])

#         return response.content