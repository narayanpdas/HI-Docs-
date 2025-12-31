import json,json5,re
import asyncio 
from schemas.chat import ChatRequest, LLMResponse
from Engine.Langchain_Engine.Engine import Engine as RAG_Engine 
from typing import AsyncGenerator,Dict,Any
import time,traceback,os
import traceback
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from db.users.session import get_func_db
from sqlalchemy import select
from models.docs import Documents
from models.guys import Guys
from services.redis_service import RedisManager

defaultcontext= """
The Digital Personal Data Protection Act (DPDP) Act is India's comprehensive data privacy law, enacted in 2023, to govern how companies and government entities handle the digital personal data of individuals. 
It requires lawful processing of data with consent, establishes rights for individuals (data principals), and outlines duties for data fiduciaries, with significant penalties for non-compliance. 
The Act is designed to protect citizen privacy while fostering a digital economy, and includes specific protections for children's data. 
"""

def clean_hipens(text):
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    return text

class RAGService:
    
    def __init__(self):
        """
            Initializes the service by creating an instance of the core RAG engine.
            This will be created once at startup, as we defined in main.py.
        """
        self.rag_engine = RAG_Engine()
        print("RAG Engine instance created for service.")
    
    def _handle_LLM_output(self,llm_outputs:list[str]):
        """Parse LLM JSON-like output safely and flexibly."""
        _temp = []
        for llm_output in llm_outputs:
            try:
                _p = json.loads(llm_output)
                _temp.append(_p)
            except json.JSONDecodeError:
                pass
            match = re.search(r"\{[\s\S]*\}", llm_output)
            if match:
                candidate = match.group(0)
                try:
                    _p = json.loads(candidate)
                    _temp.append(_p)
                except json.JSONDecodeError:
                    try:
                        _p = json5.loads(candidate)
                        _temp.append(_p)
                    except Exception:
                        pass
        return _temp
    
    def _preprocess(self,search_result):
        pattern = r'.*?\.(pdf|txt|docs)\b'
        m = set()
        # print(f's: {search_result}\n type:{type(search_result)}')
        for q in search_result[0]:
            matches = re.search(pattern,q)
            m.add(matches.group(0))
        print(f'searches: {search_result} \n m:{m}\n')
        return list(m),search_result
    
    async def search_type_requirement(self,query:str)->str:
        print(query.split(' '))
        if len(query.split(' ')) <= 8: # TODO: Make this Query Routing Logic BetTer.
            return "search"
        elif len(query.split(' ')) <= 14: 
            return 'multi-query'
        else:
            return 'decomposition'
    
    async def process_pdf(self,
                          doc_id:int,
                          user_id:str,
                          ):
        
        db:AsyncSession = get_func_db()
        user = await db.scalar(select(Guys).where(Guys.id == user_id))
        file_to_process = await db.scalar(select(Documents).where(Documents.id == doc_id))
        try:
            print(f"Processing {file_to_process.name}.")
            await self.rag_engine.load_pdf(path=file_to_process.path)
            file_to_process.is_processed = True
            user.current_process_doc_id = None
            redis_server = RedisManager()
            redis_server.delete_task(user_id=user_id)
            await redis_server.sync_credits_to_db(user_id=user_id,
                                                  db=db)
            print(f"Processing of {file_to_process.name} Complete.")
        except Exception as e:
            print("Error Occured During Processing Pdf, here\n",e)
            traceback.print_exc()
            file_to_process.is_processed = False
        finally:
            await db.commit()
            await db.close()
            
    async def search_(self,query:List[str],top_n:int,filters:List[str]=None):
        yield {"type":"thought","value":query}
        results = await self.rag_engine.search(query=query)
        print("\n ***Result From Search_ in service*** \n",results)
        yield {"type":"source","value":f"{json.dumps(obj=['Nothing Yet!'])}"}
        answer = ""
        print(type(results),type(results[0])) 
        for i in range(0,len(results)):
            answer += clean_hipens(results[i].page_content)
        yield {"type":"llm", "value":f"{answer}"}
        
    async def search(self,query:str,top_n:int,filters:List[str]):
        # cmd = await self.search_type_requirement(query= query)
        match top_n:
                case 2:
                    decomposed_query = await asyncio.to_thread(
                        self.rag_engine.decomposer._generate_decomposition,
                        query=query
                    )
                    yield {"type":"thought","value":decomposed_query}
                    _queries,_results = await asyncio.to_thread(
                                                                    self.rag_engine.seach_queries,
                                                                    queries = decomposed_query,
                                                                    top_n=5,
                                                                    filters=filters
                                                                )
                    files,file_chunks = self._preprocess(_results[0]['ids'])
                    
                    yield {"type":"search_result","value":f"{files}\n"}
                case 1:
                    query_prompt = self.rag_engine.LLM._multi_query_prompt(query=query)
                    queries = self.rag_engine.LLM.call_google(prompt=query_prompt)
                    queries = queries.split(',')
                    print(queries)
                    yield {"type":"thought","value":queries}
                    _results = await asyncio.to_thread(
                        self.rag_engine._multi_search,
                        queries= queries,
                        top_n_per_query = 2,
                        filters= filters
                    )
                    files,file_chunks = self._preprocess(_results['ids'])
                    yield {"type":"search_result","value":f"{files}\n"}
                case _:
                    _queries = query
                    yield {"type":"thought","value":[_queries]}
                    _results = await asyncio.to_thread(
                        self.rag_engine._search,
                        query = _queries,
                        top_n = 3,
                        filters=filters
                    )
                    files,file_chunks = self._preprocess(_results['ids'])
                    print(_results)
                    yield {"type":"search_result","value":f"{files}\n"}
    
    async def check_relevance(self,key,context,query):
        return self.rag_engine.LLM.check_relevance(key=key,context=context,query=query)
    
    async def get_compliance_answer(self, request: ChatRequest) -> AsyncGenerator[Dict[str,Any],None]:
        """
            Orchestrates the RAG process and ensures the output is valid.
        """
        try:
            # TODO: Hook the Seach Mode of Frontend to Search_type_requirement
            print(f"API_KEY PROVIDED: {request.api_key}")
            if request.api_key:
                try:
                    print(self.rag_engine.check_llm(key=request.api_key))
                    print(await self.check_relevance(key=request.api_key,context=defaultcontext,query=request.query))
                except BaseException as e:
                    yield{"type":"invalid_api_key",'value':"Invalid Api key Provided"}
                    print(e)
            
            async for output in self.search_(query=[request.query],top_n=request.top_n,filters=request.filters):
                print(output['type'],output['value'])
                yield{"type":output['type'],'value':output['value']}       
            
            _response = """<Default LLM Response>"""
            # yield {"type":"llm", "value":"wqdqwd"}
            # TODO: Add the LLM Call as a streaming method to get direct and better Frontend Results.
            yield {"type":"final","value":"search completed"}
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error : {e}")
            raise ValueError("Failed to parse the response from the language model.")
        except Exception as e:
            traceback.print_exc()
            print(f"Error : {e}")