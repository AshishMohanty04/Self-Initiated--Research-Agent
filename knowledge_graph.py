import streamlit as st
import networkx as nx

def init_knowledge_graph():
    if "knowledge_graph" not in st.session_state:
        st.session_state.knowledge_graph = nx.DiGraph()

def extract_knowledge_triplets(text):
    return []  # Placeholder for NLP-based triplet extraction

def build_knowledge_graph(triplets):
    for head, relation, tail in triplets:
        st.session_state.knowledge_graph.add_node(head, type="entity")
        st.session_state.knowledge_graph.add_node(tail, type="entity")
        st.session_state.knowledge_graph.add_edge(head, tail, relation=relation)
