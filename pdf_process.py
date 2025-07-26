from bangla_pdf_ocr import process_pdf
from langchain.document_loaders import TextLoader

def pdf_to_documents(pdf_path: str, txt_output_path: str = "output.txt"):
    """
    Process a Bangla PDF to extract OCR text and return LangChain documents.
    
    Args:
        pdf_path (str): Path to the PDF file.
        txt_output_path (str): Output path to save extracted text.
    
    Returns:
        list: List of LangChain Document objects.
    """
    extracted_text = process_pdf(pdf_path, txt_output_path)
    print("OCR Text Extracted Successfully.")

    # Load as LangChain Documents
    loader = TextLoader(txt_output_path, encoding="utf-8")
    documents = loader.load()
    return documents

docs = pdf_to_documents("./data/raw/HSC26-Bangla1st-Paper.pdf", "./data/extracted/HSC26-Bangla1st-Paper.txt")
