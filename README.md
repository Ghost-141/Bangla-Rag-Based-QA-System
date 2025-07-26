# Bangla Question Answering System

This is a Question Answering system that can answer questions in both Bangla and English. It uses a RAG (Retrieval-Augmented Generation) pipeline to generate answers from a processed `.pdf` file.

## Project Structure
```
├── data/
│   ├── processed/
│   │   ├── chroma_langchain_db
│   │   ├── HSC26-Bangla1st-Paper.txt
│   │   └── stopwords.pkl
│   └── raw/
│       ├── HSC26-Bangla1st-Paper.pdf
│       └── bangla_stopwords.xlsx
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
    python -m venv venv
    source venv/bin/activate 
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
