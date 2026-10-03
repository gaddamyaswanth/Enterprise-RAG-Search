import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

from llm import generate_answer


# ----------------------------
# Load data
# ----------------------------

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

with open("metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

index = faiss.read_index("vectorstore.index")

model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# BM25 Index
# ----------------------------

tokenized_chunks = [
    chunk.lower().split()
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_chunks)


# ----------------------------
# Hybrid Search
# ----------------------------

def hybrid_search(question, top_k=3):

    bm25_scores = bm25.get_scores(
        question.lower().split()
    )

    embedding = model.encode([question]).astype("float32")

    distances, ids = index.search(
        embedding,
        len(chunks)
    )

    faiss_scores = np.zeros(len(chunks))

    for rank, idx in enumerate(ids[0]):
        faiss_scores[idx] = 1 / (1 + distances[0][rank])

    bm25_scores = bm25_scores / (bm25_scores.max() + 1e-9)
    faiss_scores = faiss_scores / (faiss_scores.max() + 1e-9)

    scores = 0.5 * bm25_scores + 0.5 * faiss_scores

    best = np.argsort(scores)[::-1][:top_k]

    return best, scores


# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":

    question = input("Ask a question: ")

    results, scores = hybrid_search(question)

    context = ""

    print("\n")
    print("=" * 60)
    print("Retrieved Documents")
    print("=" * 60)

    for r in results:

        print("\n-------------------------------------")
        print("Score:", round(float(scores[r]), 3))
        print("Source:", metadata[r]["source"])
        print("Page:", metadata[r]["page"])

        context += chunks[r]
        context += "\n\n"

    print("\n")
    print("=" * 60)
    print("AI Answer")
    print("=" * 60)

    answer = generate_answer(
        question,
        context
    )

    print(answer)