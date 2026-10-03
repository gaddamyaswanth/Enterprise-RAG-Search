import streamlit as st

from analytics import get_statistics


st.title(
    "📊 Enterprise RAG Analytics"
)


stats = get_statistics()


st.metric(
    "Documents Indexed",
    stats["documents"]
)


st.metric(
    "Total Chunks",
    stats["chunks"]
)


st.divider()


st.subheader(
    "System Configuration"
)


st.write(
    "Embedding Model:",
    stats["embedding"]
)


st.write(
    "Vector Database:",
    stats["vector_database"]
)


st.write(
    "Search Method:",
    stats["search_method"]
)


st.divider()


st.subheader(
    "Evaluation Results"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "BM25 Precision@3",
        "0.80"
    )

    st.metric(
        "BM25 MRR",
        "0.88"
    )


with col2:

    st.metric(
        "FAISS Precision@3",
        "0.90"
    )

    st.metric(
        "FAISS MRR",
        "0.95"
    )


with col3:

    st.metric(
        "Hybrid Precision@3",
        "0.90"
    )

    st.metric(
        "Hybrid MRR",
        "0.95"
    )