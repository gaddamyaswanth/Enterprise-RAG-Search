import chromadb
import pickle

from sentence_transformers import SentenceTransformer


# =========================
# Load chunks
# =========================

with open("chunks.pkl", "rb") as f:
    chunks = pickle.load(f)



# =========================
# Create Chroma Database
# =========================

client = chromadb.PersistentClient(
    path="database"
)



collection = client.get_or_create_collection(
    name="enterprise_documents"
)



# =========================
# Embedding Model
# =========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# =========================
# Create Embeddings
# =========================

embeddings = model.encode(
    chunks
)



# =========================
# Store in ChromaDB
# =========================

collection.add(

    documents=chunks,

    embeddings=[
        embedding.tolist()
        for embedding in embeddings
    ],

    ids=[
        str(i)
        for i in range(len(chunks))
    ],

    metadatas=[
        {
            "source":
                "Enterprise_RAG_Company_Documents.pdf"
        }
        for _ in chunks
    ]

)



print(
    "Documents stored successfully!"
)


print(
    "Number of documents:",
    collection.count()
)