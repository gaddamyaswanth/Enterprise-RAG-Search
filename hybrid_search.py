import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi


# ==========================
# Load Chunks
# ==========================

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


# ==========================
# Load Metadata
# ==========================

with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)



# ==========================
# Load FAISS Index
# ==========================

index = faiss.read_index(
    "vectorstore.index"
)



# ==========================
# Load Embedding Model
# ==========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# ==========================
# Create BM25 Index
# ==========================

tokenized_chunks = [
    chunk.lower().split()
    for chunk in chunks
]


bm25 = BM25Okapi(
    tokenized_chunks
)



# ==========================
# Hybrid Search Function
# ==========================

def hybrid_search(query, top_k=3):


    # BM25 Search

    bm25_scores = bm25.get_scores(
        query.lower().split()
    )



    # FAISS Search

    query_embedding = model.encode(
        [query]
    )


    query_embedding = np.array(
        query_embedding
    ).astype(
        "float32"
    )


    distances, ids = index.search(
        query_embedding,
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



    # Normalize Scores

    bm25_scores = (
            bm25_scores /
            (bm25_scores.max()+1e-9)
    )


    faiss_scores = (
            faiss_scores /
            (faiss_scores.max()+1e-9)
    )



    # Combine

    hybrid_scores = (
            0.5 * bm25_scores
            +
            0.5 * faiss_scores
    )



    results = np.argsort(
        hybrid_scores
    )[::-1][:top_k]



    return results, hybrid_scores





# ==========================
# Run Search
# ==========================


if __name__ == "__main__":


    question = input(
        "Ask a question: "
    )


    results, scores = hybrid_search(
        question
    )



    print("\n")
    print("="*50)
    print("Hybrid Search Results")
    print("="*50)



    for i in results:


        print("\n--------------------------------")

        print(
            "Score:",
            round(
                float(scores[i]),
                3
            )
        )


        print("\nContent:")

        print(
            chunks[i]
        )


        print("\nSource:")

        print(
            metadata[i]["source"]
        )


        print(
            "Page:",
            metadata[i]["page"]
        )