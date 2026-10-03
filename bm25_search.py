import pickle
from rank_bm25 import BM25Okapi

# Load chunks
with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Tokenize chunks
tokenized_chunks = [chunk.lower().split() for chunk in chunks]

# Build BM25 index
bm25 = BM25Okapi(tokenized_chunks)


def bm25_search(query, top_k=3):
    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(scores, chunks),
        reverse=True,
        key=lambda x: x[0]
    )

    return ranked[:top_k]


if __name__ == "__main__":

    question = input("Ask a question: ")

    results = bm25_search(question)

    print("\nBM25 Results")
    print("=" * 40)

    for score, chunk in results:
        print(f"\nScore: {score:.2f}")
        print(chunk)
        print("-" * 40)