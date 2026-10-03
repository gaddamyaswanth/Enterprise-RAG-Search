import os
import pickle
import numpy as np
import faiss

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


DOCUMENT_FOLDER = "data/documents"


chunks = []
metadata = []


print("Processing documents...")


for file in os.listdir(DOCUMENT_FOLDER):


    if file.endswith(".pdf"):


        pdf_path = os.path.join(
            DOCUMENT_FOLDER,
            file
        )


        print(
            "Reading:",
            file
        )


        reader = PdfReader(
            pdf_path
        )


        for page_number, page in enumerate(reader.pages):


            text = page.extract_text()


            if text:


                words = text.split()


                chunk_size = 80


                for i in range(
                        0,
                        len(words),
                        chunk_size
                ):


                    chunk = " ".join(
                        words[i:i+chunk_size]
                    )


                    chunks.append(
                        chunk
                    )


                    metadata.append(
                        {
                            "source": file,
                            "page": page_number + 1
                        }
                    )



print(
    "Total chunks:",
    len(chunks)
)



# Create embeddings

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


embeddings = model.encode(
    chunks
)


embeddings = np.array(
    embeddings
).astype(
    "float32"
)



# Create FAISS index

index = faiss.IndexFlatL2(
    embeddings.shape[1]
)


index.add(
    embeddings
)



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


# Save metadata

with open(
        "metadata.pkl",
        "wb"
) as f:

    pickle.dump(
        metadata,
        f
    )


print(
    "Index created successfully!"
)