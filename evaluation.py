import pickle
import faiss
import numpy as np

from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from evaluation_data import queries


# ==============================
# Load chunks
# ==============================

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


# ==============================
# BM25 setup
# ==============================

tokenized_chunks = [
    chunk.lower().split()
    for chunk in chunks
]


bm25 = BM25Okapi(
    tokenized_chunks
)


# ==============================
# FAISS setup
# ==============================

index = faiss.read_index(
    "vectorstore.index"
)


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# ==============================
# Evaluation Metrics
# ==============================


def precision_at_k(results, keywords, k):

    correct = 0


    for result in results[:k]:

        result = result.lower()

        matches = 0


        for word in keywords:

            if word.lower() in result:
                matches += 1


        if matches >= 2:
            correct += 1


    return correct / k



def reciprocal_rank(results, keywords):

    for position, result in enumerate(results, start=1):

        result = result.lower()

        matches = 0


        for word in keywords:

            if word.lower() in result:
                matches += 1


        if matches >= 2:

            return 1 / position


    return 0



# ==============================
# Search Methods
# ==============================


def bm25_search(query, k=3):

    scores = bm25.get_scores(
        query.lower().split()
    )


    indexes = np.argsort(
        scores
    )[::-1][:k]


    return [
        chunks[i]
        for i in indexes
    ]



def faiss_search(query, k=3):

    vector = model.encode(
        [query]
    ).astype(
        "float32"
    )


    distances, indexes = index.search(
        vector,
        k
    )


    return [
        chunks[i]
        for i in indexes[0]
    ]



def hybrid_search(query, k=3):


    # BM25 scores

    bm25_scores = bm25.get_scores(
        query.lower().split()
    )


    # FAISS scores

    vector = model.encode(
        [query]
    ).astype(
        "float32"
    )


    distances, ids = index.search(
        vector,
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



    # Normalize

    bm25_norm = (
            bm25_scores /
            (bm25_scores.max()+1e-9)
    )


    faiss_norm = (
            faiss_scores /
            (faiss_scores.max()+1e-9)
    )


    # Hybrid ranking

    final_score = (
            0.5 * bm25_norm
            +
            0.5 * faiss_norm
    )


    indexes = np.argsort(
        final_score
    )[::-1][:k]


    return [
        chunks[i]
        for i in indexes
    ]



# ==============================
# Run Evaluation
# ==============================


methods = {

    "BM25": bm25_search,

    "FAISS": faiss_search,

    "Hybrid": hybrid_search

}



for name, method in methods.items():


    precision_scores = []

    mrr_scores = []


    for query, keywords in queries.items():


        results = method(query)



        precision_scores.append(

            precision_at_k(
                results,
                keywords,
                1
            )

        )


        mrr_scores.append(

            reciprocal_rank(
                results,
                keywords
            )

        )



    print("\n")
    print("="*40)

    print(name)


    print(
        "Precision@3:",
        round(
            np.mean(precision_scores),
            3
        )
    )


    print(
        "MRR:",
        round(
            np.mean(mrr_scores),
            3
        )
    )