from langchain_community.document_loaders import TextLoader

def load_documents(file_path="HSC26-Bangla1st-Paper.txt"):
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    all_text = " ".join([doc.page_content for doc in documents])
    return all_text

text = load_documents(file_path="HSC26-Bangla1st-Paper.txt")