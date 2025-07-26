from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.utils.retriever import create_bangla_qa_pipeline

app = FastAPI(
    title="Bangla QA based RAG API",
    description="API for answering Bangla questions using RAG pipeline",
    version="1.0.0"
)

qa_chain = create_bangla_qa_pipeline()

class Question(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "Bangla RAG API is up!"}

@app.post("/ask")
async def ask_question(question: Question):
    try:
        result = qa_chain.invoke(question.query)

        if isinstance(result, str):
            return {"answer": result}

        elif isinstance(result, dict) and "result" in result:
            return {"answer": result["result"]}

        else:
            return {"answer": str(result)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
