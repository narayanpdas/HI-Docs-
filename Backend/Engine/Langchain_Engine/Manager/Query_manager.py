import tensorflow as tf
from transformers import BartTokenizer, TFBartForConditionalGeneration
import os,gc,re
from typing import Callable
from dotenv import find_dotenv,load_dotenv
load_dotenv(find_dotenv('config.env')) 

INPUT_MAX_TOKEN_LEN = 128
OUTPUT_MAX_TOKEN_LEN = 256

MODEL_SAVE_PATH = os.getenv("QUERY_DECOMPOSER_MODEL_PATH")

class Query_Manager():
    def __init__(self):
        self.tokenizer = BartTokenizer.from_pretrained(MODEL_SAVE_PATH)
        self.model = TFBartForConditionalGeneration.from_pretrained(MODEL_SAVE_PATH)
    def _substitute_variables(self, query,execution_history: list):
        
        """
        Replaces internal variable references (#n) in the query string.
        Since we don't have real results, we use a clear placeholder.
        """
        pattern = r'#(\d+)'
        
        def replacement_function(match):
            index = int(match.group(1))
            history_index = index - 1
            if 1 <= index <= len(execution_history):
                print(index)
                result = execution_history[history_index] 
                return str(result)
            else:
                return match.group(0)
        return re.sub(pattern, replacement_function, query)
    def _parser(self,_decomposed_query:str):
        steps = [step.strip() for step in _decomposed_query.split(';') if step.strip()]
        templates = [step.replace('return', '', 1).strip() for step in steps]
        return templates
    def _generate_decomposition(self,query:str):
        """
        Docstring for generate_decomposition: Tokenizes a question and uses the loaded BART model for decomposition.
        
        :param: User Query
        :outputs:a List of Query(if not decomposed)/Quries
        NOTE: Model used(DEFAULT is BART) ,Tokenizer for the Model (DEFAULT is BART)
        """
        inputs = self.tokenizer(
            [query],
            max_length=INPUT_MAX_TOKEN_LEN, 
            truncation=True,
            padding="max_length",
            return_tensors="tf"
        )
        generated_ids = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=OUTPUT_MAX_TOKEN_LEN,
            num_beams=4, 
            early_stopping=True,
        )
        decomposition = self.tokenizer.decode(
            generated_ids.numpy()[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
        return self._parser(decomposition)
    def generate_all_decompositions(self,rag_search:Callable[[str,int,list,list],str],
                                    query_templates:list[str],top_n:int)->list:
        resolved_queries = []
        simulated_history = []
        for i, template in enumerate(query_templates):
            executable_query = self._substitute_variables(template, simulated_history)
            resolved_queries.append(executable_query)
            query_result = rag_search(query=executable_query,
                                    top_n=top_n,
                                    filters=None,
                                    include=['documents','metadatas'])
            simulated_history.append(query_result)
        return resolved_queries,simulated_history
