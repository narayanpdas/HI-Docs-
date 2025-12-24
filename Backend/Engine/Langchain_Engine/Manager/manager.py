from langchain_community.document_loaders import UnstructuredPDFLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_core.documents import Document
from dotenv import load_dotenv, find_dotenv
import pandas as pd
import  os, asyncio
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_community.embeddings import HuggingFaceEmbeddings
# TODO Add Pydantic Class here for better Control of .env Variables.
load_dotenv(find_dotenv('config.env'))
ENCODER_MODEL = os.getenv('ENCODER_NAME', 'all-MiniLM-L6-v2')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'test')
PDF_PATH = os.getenv('PDF_PATH')
VECTORDB_PATH = os.getenv('VECTORDB_PATH','vector_db')
NOISE_FILTER_MODEL_PATH = os.getenv('NOISE_FILTER_MODEL_PATH', 'madhurjindal/autonlp-Gibberish-Detector-492513457')
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 250))
CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 50))
MANIFEST_PATH = os.getenv("MANIFEST_PATH")


class Manager():
    def __init__(self):
        self._pdf_path = PDF_PATH
        self.gibberish_filter_path = NOISE_FILTER_MODEL_PATH
        self.encoder = HuggingFaceEmbeddings(model_name = ENCODER_MODEL,
                                            encode_kwargs={'normalize_embeddings': True},
                                            )
                                            # query_instruction="Represent this sentence for searching relevant passages: ")
        self.filter_model, self.filter_tokenizer = self._load_filter_model()
        self.chroma = Chroma(
                            collection_name=COLLECTION_NAME,
                            persist_directory=VECTORDB_PATH,
                            embedding_function=self.encoder
                            )
        # self.bm25 = BM25Retriever()
        self.bm25retriever = None
        self.chromaretriever = None
    
    def _load_filter_model(self):
        model = AutoModelForSequenceClassification.from_pretrained(self.gibberish_filter_path)
        tokenizer = AutoTokenizer.from_pretrained(self.gibberish_filter_path)
        return model, tokenizer
    
    def _is_noise(self, text, model, tokenizer):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_label_id = probabilities.argmax().item()
        label = model.config.id2label[predicted_label_id]
        return label == 'noise'
    
    async def load_pdf(self,path:str):
        _pages =  await self._load_pages(path=path)
        # print("Pages: \n",_pages)
        return await self._load_to_space(pages =_pages)
    
    async def _load_pages(self, path: str):
        loader = UnstructuredPDFLoader(
                                    file_path=path, 
                                    max_characters=1800,
                                    new_after_n_chars=1500,
                                    mode="elements",
                                    # strategy="fast",
                                    chunking_strategy="by_title",
                                    combine_text_under_n_chars=200,
                                    overlap=200,
                                    )
        
        pages = await loader.aload()
        _elements = ["NarrativeText", "ListItem", "Title","CompositeElement"]
        print("\nPAGES\n",pages)
        # print("PAGES\n",pages)
        filtered_pages = [doc for doc in pages if doc.metadata.get('category') in _elements]
        print("FILTERED PAGES\n",filtered_pages)
        
        # _results = await asyncio.to_thread(self._is_noise,
        #                             filtered_pages,self.filter_model,self.filter_tokenizer)
        return filter_complex_metadata(filtered_pages)

    async def _load_to_space(self,pages:list[Document]):
        await self.chroma.aadd_documents(documents=pages)
        self.chromaretriever = self.chroma.as_retriever(search_kwargs={'k':3})
        # bm25_retriever = self.bm25.from_documents(documents=pages)
        # self.bm25retriever = bm25_retriever
        return True

    def _pretty_print(self, docs: list[Document], to_save: bool = False):
        _data = [
            {
                'content': doc.page_content,
                'page_number': doc.metadata.get('page_number'),
                'category': doc.metadata.get('category'),
                'doc_len': len(doc.page_content)
            }
            for doc in docs
        ]
        df = pd.DataFrame(data=_data)
        pd.set_option('display.max_colwidth', None)
        if to_save:
            df.to_json('doc.json')
        return df
