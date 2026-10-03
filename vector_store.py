import faiss
import pickle

from embedding import create_embeddings
from chunking import split_text
from pdf_loader import load_pdf


PDF_PATH = "data/documents/Enterprise_RAG_Company_Documents.pdf"


print("Loading PDF...")

text = load_pdf(PDF_PATH)


print("Creating chunks...")

chunks = split_text(text)


print("Creating embeddings...")

embeddings = create_embeddings(chunks)


# Convert to float32 for FAISS
embeddings = embeddings.astype("float32")


print("Creating FAISS index...")


dimension = embeddings.shape[1]


index = faiss.IndexFlatL2(dimension)


index.add(embeddings)


print("FAISS index created!")

print("Number of vectors:")
print(index.ntotal)



# Save index

faiss.write_index(
    index,
    "vectorstore.index"
)


# Save chunks

with open(
        "chunks.pkl",
        "wb"
) as f:

    pickle.dump(
        chunks,
        f
    )


print("Saved successfully!")