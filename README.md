

# 🤖 Self-Initiated Research Agent

An **autonomous multi-agent research system** built with **Streamlit**.
It can search the web, extract text, summarize results into **note-style points**, fact-check sources, build a knowledge graph, and generate a **PDF research report**.
It also has a **memory module** powered by FAISS to recall past queries.

---

## ✨ Features

* 🔍 **Web Search** — Uses DuckDuckGo to find relevant sources.
* 📄 **Text Extraction** — Extracts clean article text from web pages.
* 📝 **Summarization (Note-Style)** — Generates well-formatted bullet point summaries.
* ✅ **Critic Agent** — Assigns a confidence score based on source reliability.
* 🧠 **Memory (FAISS Vector DB)** — Stores embeddings of past queries for retrieval.
* 🌐 **Knowledge Graph** — Builds connections between extracted knowledge (future-ready).
* 📑 **PDF Report Generation** — Automatically generates a structured research report with findings & references.
* 💡 **Follow-up Queries** — Ask new questions based on past research.

---

## 📂 Project Structure

```
research_agent/
│── app.py                # Main Streamlit app
│── agents.py             # Retriever, summarizer, critic agents
│── memory.py             # Memory search with FAISS
│── knowledge_graph.py    # Knowledge graph builder
│── report.py             # PDF report & citation generator
│── models.py             # Model loading (Summarizer + Embeddings)
│── utils.py              # Helper functions (text extraction, query breakdown, etc.)
│── requirements.txt      # Dependencies
│── README.md             # This file
```

---

## ⚡ Installation

### 1️⃣ Clone the Repository

```bash
[git clone https://github.com/your-username/research-agent.git
cd research-agent](https://github.com/AshishMohanty04/Self-Initiated--Research-Agent.git)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open your browser at **[http://localhost:8501/](http://localhost:8501/)** 🎉

---

## 🛠 Tech Stack

* **Frontend/UI** → [Streamlit](https://streamlit.io/)
* **Search Engine** → [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)
* **Text Extraction** → [Trafilatura](https://pypi.org/project/trafilatura/)
* **Summarization** → [Transformers](https://huggingface.co/docs/transformers/) (BART-Large-CNN)
* **Embeddings + Memory** → [SentenceTransformers](https://www.sbert.net/) + [FAISS](https://github.com/facebookresearch/faiss)
* **Knowledge Graph** → [NetworkX](https://networkx.org/)
* **Report Generation** → [FPDF](https://pyfpdf.github.io/fpdf2/)
* **Citations** → [Pybtex](https://pybtex.org/)

---

## 📑 Example Workflow

1. Enter a **research query** (e.g., *"Impact of AI on Healthcare"*)
2. The system breaks it into **sub-questions**
3. Searches the web for reliable sources
4. Extracts text & generates **note-style summaries**
5. Assigns confidence scores
6. Builds a **knowledge graph** (future expansion)
7. Generates a **PDF report** with findings & references
8. Stores data in **memory** for follow-up queries

---

## 📌 Roadmap

* [ ] Improve **knowledge graph triplet extraction**
* [ ] Add **multi-modal support** (images, tables)
* [ ] Enhance **memory retrieval** with RAG (Retrieval-Augmented Generation)
* [ ] Deploy on **Streamlit Cloud / AWS**

---



