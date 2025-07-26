import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")

def get_api_key():
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    return groq_api_key if groq_api_key else print("GROQ_API_KEY not found in environment variables.")
  

# custom_prompt = PromptTemplate(
#     input_variables=["context", "question"],
#     template=(
#         "নিচের তথ্যটি মনোযোগ দিয়ে পড়ুন এবং প্রশ্নের উত্তর দিন। "
#         "তথ্য ছাড়া অনুমান করবেন না। শুধুমাত্র সঠিক উত্তর দিন।\n\n"
#         "তথ্য:\n{context}\n\n"
#         "প্রশ্ন: {question}\n"
#         "উত্তর:"
#     )
# )


custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=(
        "Read the following context carefully and answer the question. "
        "The question may be in Bangla, English. "
        "Answer strictly based on the context without making assumptions. Just provide answer, don't assume anyhting.\n\n"
        "Respond in the same language as the question.\n\n"

        # Few-shot Example 1: English
        "Example 1 (English):\n"
        "Context:\nBangladesh became an independent country in 1971 after a war of liberation.\n"
        "Question: When did Bangladesh gain independence?\n"
        "Answer: Bangladesh gained independence in 1971.\n\n"

        # Few-shot Example 2: Bangla
        "Example 2 (Bangla):\n"
        "Context:\nকাজী নজরুল ইসলাম বাংলাদেশের জাতীয় কবি। তিনি বিদ্রোহী কবি নামেও পরিচিত।\n"
        "প্রশ্ন: বাংলাদেশের জাতীয় কবি কে?\n"
        "উত্তর: বাংলাদেশের জাতীয় কবি কাজী নজরুল ইসলাম।\n\n"

        # Actual Input
        "Now answer the following:\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    )
)

def create_bangla_qa_pipeline(api_key=None):
    """
    Initializes and returns a RetrievalQA pipeline using:
    - Chroma DB for retrieval (with banBERT embeddings),
    - ChatGroq with the Gemma-2-9B-IT model for generation,
    - Custom prompt for Bengali PDF-based QA.
    Returns:
        RetrievalQA: A LangChain RetrievalQA chain ready for use.
    """
    if api_key is None:
        api_key = get_api_key()
        if not api_key:
            raise ValueError("API key is required but not provided.")
        
    retriever = Chroma(
        collection_name="bangla-pdf-base",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db"
    ).as_retriever()

    chat = ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0,
        max_retries=3,
        api_key=api_key,
    )

    qa = RetrievalQA.from_chain_type(
        llm=chat,
        retriever=retriever,
        chain_type_kwargs={"prompt": custom_prompt}
    )

    return qa

