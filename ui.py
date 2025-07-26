import streamlit as st
import requests

st.set_page_config(page_title="RAG Powerd QA System", layout="centered")

st.title("Bangla Question Answering System")

st.write("Click on a sample question below:")

sample_questions = [
    "কাকে অনুপমের ভাগ্য দেবতা বলে উল্লেখ করা হয়েছে?",
    "বিয়ের সময় কল্যাণীর প্রকৃত বয়স কত ছিল?",
    "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
    "কল্যানীর বাবার নাম কি?",
    "What was the Age of Kalyani at the time of marriage?"
]

selected_sample = st.selectbox("Sample questions:", [""] + sample_questions)

question = st.text_input("Your question in Bangla or English:", value=selected_sample if selected_sample else "")

if st.button("Get Answer") and question:
    with st.spinner("Generating answer..."):
        try:
            response = requests.post(
                "http://localhost:8000/ask",  
                json={"query": question}
            )
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer found.")
                st.success(f"**Answer:** {answer}")
            else:
                st.error("Failed to get answer from the backend.")
        except Exception as e:
            st.error(f"Error: {e}")