# Bangla Question Answering System

This is a Q/A based system that can answer questions in both Bangla and English. It uses a RAG (Retrieval-Augmented Generation) pipeline to generate answers from a processed `.pdf` file.

## Project Structure
```
├── data/
│   ├── processed/
│   │   ├── HSC26-Bangla1st-Paper.txt
│   │   └── stopwords.pkl
│   └── raw/
│       ├── HSC26-Bangla1st-Paper.pdf
│       └── bangla_stopwords.xlsx
├── chroma_langchain_db/
├── notebook/
│   └── test.ipynb
├── src/
│   └── utils/
│       ├── dataloader.py
│       ├── datastore.py
│       ├── preprocess.py
│       └── retriever.py
├── api.py
├── ui.py
├── requirements.txt
├── README.md
└── .env
```

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/bangla-qa-system.git
    cd bangla-qa-system
    ```

2.  **Create a virtual environment:**
    #### Using `venv`:
    ```bash
    python3.9 -m venv rag
    rag/bin/activate #for windows
    source rag/bin/activate #for linux 
    ```
    #### Using `anaconda`:
    ```bash
    #using conda
    conda create -n rag python=3.9
    conda activate rag
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Go to [groq](https://console.groq.com/home?utm_source=website&utm_medium=outbound_link&utm_campaign=dev_console_click) official website and create an account. Go to `API Keys` and `Create API Key`. Copy the api key.

    Create a `.env` file in the root directory and add your Groq API key as following:
    ```
    GROQ_API_KEY=paste_api_key_here
    ```

## Usage

The project has two main components: a backend API built with FastAPI and a frontend user interface built with Streamlit.

### Backend

To run the backend server, execute the following command:
```bash
uvicorn api:app --reload
```
This will start the server at `http://localhost:8000`.

### Frontend

To run the frontend application, execute the following command:
```bash
streamlit run ui.py
```
This will open the user interface in your web browser.

## API Documentation

The API provides an endpoint for answering questions.

### POST `/ask`

This endpoint takes a JSON object with a "query" field and returns a JSON object with an "answer" field.

**Request Body:**
```json
{
  "query": "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?"
}
```

**Response:**
```json
{
  "answer": "১৫ বছর"
}
```

**Example using cURL:**
```bash
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{"query": "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?"}'
```

## Libraies Used

- LangChain
- Huggingface
- fastapi
- streamlit

## Qestion-Answer

**What method or library did you use to extract the text, and why? Did you face any formatting challenges with the PDF content?**    

*Ans:* I have used ocr based mathod to extract text from the pdf as normal function of langchain pdf to text fails to extract text properly. After that, I have exported the extracted text to `.txt` file and used langchain `TextLoader` function to load the text files.

The pdf contains different structuers in different page including different encoding format of text. So, it difficult to extract all the text properly preserving the document format.

**What chunking strategy did you choose (e.g. paragraph-based, sentence-based, character limit)? Why do you think it works well for semantic retrieval?**

*Ans:* I have used sentence based chunking. The document contains stories and different plots of the stories. So, word based splitting will fail to preserve the context. On the other hand, sentence based splitting can help preserve context with overlap.   

A group of sentence can preserve context compared to words. Thus concataning multiple sentences helps RAG to find context based on query.

**What embedding model did you use? Why did you choose it? How does it capture the meaning of the text?**  
*Ans:* I have used the `intfloat/multilingual-e5-base` multi-modal embedding model from huggingface.

As, my data contains both text including english and bangla. Also, my system need to answer query both in Bengali and English language, so I have choosen this modele.  

It captures meaning of the text based on the following techniques:
- BERT style encoder reads entire sentence and give attention to relationships between tokens to make rich context.
- E5 architectre is designed for dense retieval task such as RAG.
- Generates a single dense vector for entire sentence to preserve meaning and context.

**How are you comparing the query with your stored chunks? Why did you choose this similarity method and storage setup?**  
*Ans:* The query comparison with stored chunks was done using vector similarity search as following:
- User query is sent to the same embedding model and converted to dense vector embedding.
- The `Chroma` vector store contains pre-computed embeddings of all story chunks. The query embeddig is compared with these using default `cosine similarity` search to find the most similar information.
- The retivers retrives the top-k most similar chunks to the chat model as context for answering query.

Reasons to choose cosine similarity seach:
- Focuses on semantics search measuring angle
- Works well on dense embeddings based on our selected embedding model
- Ensures semantically similar queries and chunks are retrived even they don't share similart or exact words.

**How do you ensure that the question and the document chunks are compared meaningfully? What would happen if the query is vague or missing context?**  
*Ans:* The chunks are compared menaingfully as following: 
- The query and document is processed with the same embedding models tha converts both of them to vector space based on semantic meaning
- Chroma stored the vector respresentation in a vector index
- Recieved query is compare with stored vectors using cosine similarity ti retrieve the most relevant answer.
- The retrived chunks are passed to the LLM along with custom prompt regarding how to structure the answer based on query.

If the query us vauge or missing the model replies with:
- No context is given regarding the query
- Sometiems generates false or confusing answer

**Do the results seem relevant? If not, what might improve them (e.g. better chunking, better embedding model, larger document)?**  
*Ans:* On the context of given response, the model performs well and can find relevant information well. However, in some cases it might fail to generate or find relevant answer to user query.

To improve the accuracy, we can do the following things:
- Use better embedding models trained on recent dataset for better context.
- Use better pdf to text processig to maintain the structure of the data after conversion.
- Prepare text file with relevant infromation rather than vauge things.
- Improve chunking by taking more larger chunk.
- Switch to other vector store system like FAISS and so on.




