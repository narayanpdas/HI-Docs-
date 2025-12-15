from dotenv import load_dotenv,find_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from Engine.Langchain_Engine.Manager.manager import Manager
# from langsmith import client
from langchain.retrievers import EnsembleRetriever
from langchain_core.messages import HumanMessage

import os,asyncio

MULTI_QUERY_PROMPT = """
You are an AI language model assistant. Your task is to generate 1 - 5 different sub questions OR alternate versions of the given user question to retrieve relevant documents from a vector database.

By generating multiple versions of the user question,
your goal is to help the user overcome some of the limitations
of distance-based similarity search.

By generating sub questions, you can break down questions that refer to multiple concepts into distinct questions. This will help you get the relevant documents for constructing a final answer

If multiple concepts are present in the question, you should break into sub questions, with one question for each concept

Provide these alternative questions separated by newlines between XML tags. For example:

<questions>
- Question 1
- Question 2
- Question 3
</questions>

Original question: {question}
"""

load_dotenv(find_dotenv('config.env'))
GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME','gemini-2.5-flash')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ENCODER_NAME = os.getenv("ENCODER_NAME")

class Engine():
    def __init__(self):
        self.manager = Manager()
        self.API_KEY = GEMINI_API_KEY
    
    async def search(self,query:list[str],filters:list=None):
        retriever = EnsembleRetriever(retrievers=[
            self.manager.chroma.as_retriever(search_kwargs={'k':3}),
        ])
        results = await retriever.ainvoke(query[0])
        print("\n ***Result From search in engine of 1st doc*** \n",results[0].page_content)
        if filters:
            filtered = [res for res in results if res.metadata.file_name in filters]
            return filtered
        return results
    async def invoke_llm(self,prompt):
        llm = ChatGoogleGenerativeAI(
            model="gemini-flash",
            temperature=0.7,
            top_p=0.05,
            google_api_key=self.API_KEY
        )
        messages=[HumanMessage(content=prompt)]
        print("QUERY: ",messages)
        response = await llm.ainvoke(messages)
        print("LLM_RESPONSE",response.content)
        return response.content
    async def multi_query(self,query:str):
        prompt = MULTI_QUERY_PROMPT.format(question=query)
        return await self.invoke_llm(prompt=prompt)
    async def load_pdf(self,path:str):
        return await self.manager.load_pdf(path=path)
    