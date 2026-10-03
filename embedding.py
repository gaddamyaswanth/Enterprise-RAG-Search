from sentence_transformers import SentenceTransformer
from chunking import split_text
from pdf_loader import load_pdf


PDF_PATH = "data/documents/Enterprise_RAG_Company_Documents.pdf"


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings(chunks):

    embeddings = model.encode(
        chunks
    )

    return embeddings



if __name__ == "__main__":

    print("Loading PDF...")

    text = load_pdf(PDF_PATH)


    print("Creating chunks...")

    chunks = split_text(text)


    print("Generating embeddings...")


    embeddings = create_embeddings(chunks)


    print("\nEmbedding created successfully!")


    print("Number of chunks:")
    print(len(embeddings))


    print("\nVector size:")
    print(embeddings.shape)