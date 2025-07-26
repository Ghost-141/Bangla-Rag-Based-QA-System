import re
import joblib
import unicodedata

stopwords = joblib.load('data/processed/stopwords.pkl')

def remove_stopwords(text):
    words = text.split()
    filtered = [word for word in words if word not in stopwords]
    return " ".join(filtered)

def bangla_sentence_split(text):
    return re.split(r"(?<=[।!?])\s+", text.strip())

def clean_bangla_text(text):

    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[a-zA-Z0-9]", "", text)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"[“”\"\'\(\)\[\]\{\}<>\|;:…~`_+=@#$%^&*\\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def bangla_chunker(texts, chunk_size:int, chunk_overlap:int): 
    sentences = bangla_sentence_split("".join(texts))
    chunks = []
    current_chunk = []
    total_len = 0

    for sent in sentences:
        sent_len = len(sent)
        if total_len + sent_len <= chunk_size:
            current_chunk.append(sent)
            total_len += sent_len
        else:
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)

            overlap_text = chunk_text[-chunk_overlap:]

            current_chunk = [overlap_text + " " + sent]
            total_len = len(current_chunk[0])

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def preprocess_and_chunk(text, chunk_size=500, chunk_overlap=70):
    cleaned = clean_bangla_text(text)
    filtered = remove_stopwords(cleaned)
    chunks = bangla_chunker([filtered], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunks