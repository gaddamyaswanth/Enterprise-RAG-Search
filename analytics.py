import pickle
import os


def get_statistics():

    stats = {}

    # Documents

    if os.path.exists("metadata.pkl"):

        with open(
                "metadata.pkl",
                "rb"
        ) as f:

            metadata = pickle.load(f)


        documents = set(
            item["source"]
            for item in metadata
        )


        stats["documents"] = len(
            documents
        )


        stats["chunks"] = len(
            metadata
        )


    else:

        stats["documents"] = 0
        stats["chunks"] = 0



    stats["embedding"] = (
        "all-MiniLM-L6-v2"
    )


    stats["vector_database"] = (
        "FAISS"
    )


    stats["search_method"] = (
        "BM25 + FAISS Hybrid"
    )


    return stats