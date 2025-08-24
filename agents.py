from duckduckgo_search import DDGS
import streamlit as st

def retriever_agent(query, max_results=3, region="us-en"):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results, region=region):
            results.append({"title": r["title"], "link": r["href"]})
    return results

def summarizer_agent(summarizer, text, max_chunk=800):
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
