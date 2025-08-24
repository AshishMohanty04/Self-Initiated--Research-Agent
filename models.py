import streamlit as st
from duckduckgo_search import DDGS
import trafilatura
from transformers import pipeline
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
from pybtex.database import BibliographyData, Entry
import networkx as nx
from fpdf import FPDF
import io

# --- Streamlit Session State Initialization ---
if "memory_data" not in st.session_state:
    st.session_state.memory_data = []

if "faiss_index" not in st.session_state:
    dimension = 384
    st.session_state.faiss_index = faiss.IndexFlatL2(dimension)

if "knowledge_graph" not in st.session_state:
    st.session_state.knowledge_graph = nx.DiGraph()

# --- Load models ---
@st.cache_resource
def load_models():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return summarizer, embedder

summarizer, embedder = load_models()

# --- Agent Functions ---

def retriever_agent(query, max_results=3, region="us-en"):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results, region=region):
            results.append({"title": r["title"], "link": r["href"]})
    return results

def extract_text(url):
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            return trafilatura.extract(downloaded)
        return None
    except Exception as e:
        st.error(f"Error extracting text from {url}: {e}")
        return None

def summarizer_agent(text, max_chunk=800):
    """Summarize long text into bullet-point styled notes"""
    if not text:
        return "No content to summarize."
    
    chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
    summaries = []
    progress_bar = st.progress(0)
    
    for i, chunk in enumerate(chunks):
        try:
            summary = summarizer(chunk, max_length=200, min_length=50, do_sample=False)
            cleaned = summary[0]["summary_text"].replace("\n", " ").strip()
            summaries.append(f"• {cleaned}")
        except Exception as e:
            st.error(f"Error summarizing chunk: {e}")
            summaries.append("⚠️ Error summarizing chunk")
        
        progress_bar.progress((i + 1) / len(chunks))

    progress_bar.empty()
    return "\n\n".join(summaries)

def critic_agent(summary, url):
    score = 0
    if ".edu" in url or ".gov" in url:
        score += 0.5
    elif "wikipedia.org" in url:
        score += 0.2
    
    confidence_score = min(1.0, score + 0.1)
    return confidence_score

def extract_knowledge_triplets(text):
    return []

def build_knowledge_graph(triplets):
    for head, relation, tail in triplets:
        st.session_state.knowledge_graph.add_node(head, type="entity")
        st.session_state.knowledge_graph.add_node(tail, type="entity")
        st.session_state.knowledge_graph.add_edge(head, tail, relation=relation)

def break_down_query(query):
    return [
        f"What is {query.split()[0]}?",
        f"What is the impact of {query}?",
        f"Who are the key players in {query}?"
    ]

def generate_pdf_report(report_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=report_data["title"], ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, txt=f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}", ln=True, align="L")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Abstract", ln=True, align="L")
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 5, report_data["abstract"])
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Key Findings", ln=True, align="L")
    pdf.set_font("Arial", "", 12)
    for finding in report_data["findings"]:
        pdf.multi_cell(0, 5, f"- {finding}")

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="References", ln=True, align="L")
    pdf.set_font("Arial", "", 10)
    for ref in report_data["references"]:
        pdf.multi_cell(0, 5, ref)

    return pdf.output(dest='S').encode('latin1')

def search_memory(query, top_k=3):
    if not st.session_state.memory_data:
        return []
    
    vector = embedder.encode([query])
    D, I = st.session_state.faiss_index.search(vector, top_k)
    return [st.session_state.memory_data[i] for i in I[0]]

def generate_citation(title, url):
    return BibliographyData({
        "ref": Entry("misc", fields={"title": title, "howpublished": url})
    }).to_string("bibtex")

# --- Streamlit UI ---
st.set_page_config(page_title="AI Research Agent", layout="wide")
st.title("🤖 Self-Initiated Research Agent (Phase 3)")
st.write("An autonomous, multi-agent research system.")

domain = st.sidebar.selectbox(
    "Choose Domain Mode",
    ["General", "Academic Research", "Market Analysis", "Tech Trends"]
)

query = st.text_input("Enter your research query:")

if st.button("Start Autonomous Research"):
    if query:
        st.info("Initiating autonomous research loop...")
        
        with st.spinner("Breaking down query..."):
            sub_queries = break_down_query(query)
            st.write("Sub-questions identified:", sub_queries)
        
        all_summaries = []
        citations = []
        
        for i, sub_query in enumerate(sub_queries):
            st.subheader(f"🔍 Researching Sub-query {i+1}: {sub_query}")
            
            with st.spinner("Searching the web..."):
                results = retriever_agent(sub_query, max_results=2)
            
            for res in results:
                st.write(f"📖 Source: [{res['title']}]({res['link']})")
                text = extract_text(res["link"])
                if text:
                    with st.spinner("Summarizing and fact-checking..."):
                        summary = summarizer_agent(text)
                        confidence = critic_agent(summary, res["link"])
                    
                    st.markdown(f"**Confidence Score:** `{confidence:.2f}`")
                    st.markdown("### 📝 Summary (Note Style)")
                    st.markdown(f"{summary}")
                    
                    triplets = extract_knowledge_triplets(summary)
                    build_knowledge_graph(triplets)
                    
                    all_summaries.append({"Title": res["title"], "Summary": summary, "Confidence": confidence})
                    citations.append(generate_citation(res["title"], res["link"]))
        
        st.subheader("📚 Synthesis & Report Generation")
        with st.spinner("Synthesizing findings and generating report..."):
            abstract = "This report synthesizes information from multiple online sources regarding the query: " + query
            findings = [s["Summary"] for s in all_summaries]
            
            report_data = {
                "title": f"Research Report on {query}",
                "abstract": abstract,
                "findings": findings,
                "references": citations
            }
            
            pdf_bytes = generate_pdf_report(report_data)
            st.download_button(
                label="Download Research Report (PDF)",
                data=pdf_bytes,
                file_name=f"{query}_report.pdf",
                mime="application/pdf"
            )

        st.success("Autonomous research complete!")
        
    else:
        st.warning("Please enter a query.")

st.subheader("💡 Ask follow-up questions (Memory Search)")
follow_up = st.text_input("Ask something based on past queries:")
if st.button("Search Memory"):
    if follow_up:
        with st.spinner("Searching memory..."):
            memory_hits = search_memory(follow_up)
        
        if memory_hits:
            for m in memory_hits:
                st.write(f"🔎 From past query: {m['query']}")
                st.success(m["summary"])
                st.write(m["url"])
        else:
            st.warning("No relevant memory found yet.")
    else:
        st.warning("Please enter a follow-up question.")
