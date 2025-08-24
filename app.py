import streamlit as st
from models import load_models
from agents import retriever_agent, summarizer_agent, critic_agent
from memory import init_memory, search_memory
from knowledge_graph import init_knowledge_graph, extract_knowledge_triplets, build_knowledge_graph
from report import generate_pdf_report, generate_citation
from utils import extract_text, break_down_query

# --- Initialization ---
st.set_page_config(page_title="AI Research Agent", layout="wide")
st.title("🤖 Self-Initiated Research Agent (Phase 3)")
st.write("An autonomous, multi-agent research system.")

# Init components
init_memory()
init_knowledge_graph()

# Load models
summarizer, embedder = load_models()

# --- Sidebar ---
domain = st.sidebar.selectbox(
    "Choose Domain Mode",
    ["General", "Academic Research", "Market Analysis", "Tech Trends"]
)

# --- Main Research Loop ---
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
                        summary = summarizer_agent(summarizer, text)
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

# --- Memory Search ---
st.subheader("💡 Ask follow-up questions (Memory Search)")
follow_up = st.text_input("Ask something based on past queries:")
if st.button("Search Memory"):
    if follow_up:
        with st.spinner("Searching memory..."):
            memory_hits = search_memory(embedder, follow_up)
        
        if memory_hits:
            for m in memory_hits:
                st.write(f"🔎 From past query: {m['query']}")
                st.success(m["summary"])
                st.write(m["url"])
        else:
            st.warning("No relevant memory found yet.")
    else:
        st.warning("Please enter a follow-up question.")
