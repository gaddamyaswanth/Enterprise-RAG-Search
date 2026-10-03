import streamlit as st
import pickle
import faiss
import numpy as np
import os

from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

from llm import generate_answer
from document_manager import process_documents
from query_expansion import expand_query


# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==========================
# Chat Memory
# ==========================

if "messages" not in st.session_state:
    st.session_state.messages = []



# ==========================
# Load System
# ==========================

@st.cache_resource
def load_system():

    with open(
            "chunks.pkl",
            "rb"
    ) as f:
        chunks = pickle.load(f)


    with open(
            "metadata.pkl",
            "rb"
    ) as f:
        metadata = pickle.load(f)


    index = faiss.read_index(
        "vectorstore.index"
    )


    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


    tokenized = [
        chunk.lower().split()
        for chunk in chunks
    ]


    bm25 = BM25Okapi(
        tokenized
    )


    return (
        chunks,
        metadata,
        index,
        model,
        bm25
    )



# ==========================
# Hybrid Search
# ==========================

def hybrid_search(
        query,
        chunks,
        index,
        model,
        bm25,
        top_k=3
):


    bm25_scores = bm25.get_scores(
        query.lower().split()
    )


    embedding = model.encode(
        [query]
    ).astype(
        "float32"
    )


    distances, ids = index.search(
        embedding,
        len(chunks)
    )


    faiss_scores = np.zeros(
        len(chunks)
    )


    for rank, idx in enumerate(ids[0]):

        faiss_scores[idx] = (
                1 /
                (1 + distances[0][rank])
        )


    if bm25_scores.max() != 0:

        bm25_scores = (
                bm25_scores /
                bm25_scores.max()
        )


    if faiss_scores.max() != 0:

        faiss_scores = (
                faiss_scores /
                faiss_scores.max()
        )


    final_scores = (
            0.5 * bm25_scores
            +
            0.5 * faiss_scores
    )


    results = np.argsort(
        final_scores
    )[::-1][:top_k]


    return results, final_scores



# ==========================
# Sidebar Upload
# ==========================

with st.sidebar:


    st.title(
        "📂 Document Upload"
    )


    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type="pdf",
        accept_multiple_files=True
    )


    if uploaded_files:


        os.makedirs(
            "data/documents",
            exist_ok=True
        )


        for file in uploaded_files:


            path = os.path.join(
                "data/documents",
                file.name
            )


            with open(
                    path,
                    "wb"
            ) as f:

                f.write(
                    file.getbuffer()
                )


        st.success(
            "PDF uploaded successfully"
        )


        if st.button(
                "Create Index"
        ):


            with st.spinner(
                    "Processing documents..."
            ):


                total = process_documents()


            st.success(
                f"Indexed {total} chunks"
            )


            st.cache_resource.clear()



    st.divider()


    if st.button(
            "🗑 Clear Chat"
    ):

        st.session_state.messages = []

        st.rerun()



# ==========================
# Main Application
# ==========================

st.title(
    "🤖 Enterprise AI Document Assistant"
)


st.caption(
    "Hybrid Retrieval + Query Expansion + RAG"
)



try:

    chunks, metadata, index, model, bm25 = load_system()


except Exception:

    st.warning(
        "Upload documents and create index first."
    )

    st.stop()



# Display previous messages

for message in st.session_state.messages:


    with st.chat_message(
            message["role"]
    ):

        st.write(
            message["content"]
        )



# Chat input

question = st.chat_input(
    "Ask about your documents..."
)



if question:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    with st.chat_message(
            "user"
    ):

        st.write(
            question
        )



    with st.chat_message(
            "assistant"
    ):


        with st.spinner(
                "Searching documents..."
        ):


            # Query Expansion

            expanded_question = expand_query(
                question
            )


            results, scores = hybrid_search(
                expanded_question,
                chunks,
                index,
                model,
                bm25
            )


            context = ""

            sources = []


            for r in results:


                context += chunks[r]

                context += "\n\n"


                sources.append(
                    {
                        "file":
                            metadata[r]["source"],

                        "page":
                            metadata[r]["page"],

                        "score":
                            round(
                                float(scores[r]),
                                3
                            )
                    }
                )



            answer = generate_answer(
                question,
                context
            )


            st.write(
                answer
            )


            st.divider()


            st.write(
                "📚 Sources"
            )


            for source in sources:

                st.write(
                    f"""
📄 {source['file']}

Page:
{source['page']}

Score:
{source['score']}
"""
                )



    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )