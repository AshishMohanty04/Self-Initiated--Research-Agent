import trafilatura
import streamlit as st

def extract_text(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded)
        return None
    except Exception as e:
        st.error(f"Error extracting text from {url}: {e}")
        return None

def break_down_query(query):
    return [
        f"What is {query.split()[0]}?",
        f"What is the impact of {query}?",
        f"Who are the key players in {query}?"
    ]
