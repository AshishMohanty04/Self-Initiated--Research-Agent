import streamlit as st
import faiss

def init_memory(dimension=384):
    if "memory_data" not in st.session_state:
        st.session_state.memory_data = []
    if "faiss_index" not in st.session_state:
        st.session_state.faiss_index = faiss.IndexFlatL2(dimension)

def search_memory(embedder, query, top_k=3):
    if not st.session_state.memory_data:
        return []
    vector = embedder.encode([query])
    D, I = st.session_state.faiss_index.search(vector, top_k)
    return [st.session_state.memory_data[i] for i in I[0]]
