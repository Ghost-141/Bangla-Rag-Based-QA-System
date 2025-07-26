from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")

vector_store = Chroma(
    collection_name="bangla-pdf-base",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  
)