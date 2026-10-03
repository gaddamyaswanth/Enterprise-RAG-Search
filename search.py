import faiss
import pickle

from sentence_transformers import SentenceTransformer


# Load FAISS index

index = faiss.read_index(
    "vectorstore.index"
)


# Load chunks

with open(
        "chunks.pkl",
        "rb"
) as f:

    chunks = pickle.load(f)



# Load embedding model

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



def search(query, k=2):

    # Convert query to vector

    query_vector = model.encode(
        [query]
    )


    query_vector = query_vector.astype(
        "float32"
    )


    # Search FAISS

    distances, indexes = index.search(
        query_vector,
        k
    )


    results = []


    for i in indexes[0]:

        results.append(
            chunks[i]
        )


    return results



if __name__ == "__main__":


    question = input(
        "Ask a question: "
    )


    results = search(
        question
    )


    print("\nRelevant Information:")
    print("----------------------")


    for result in results:

        print(result)
        print("\n")