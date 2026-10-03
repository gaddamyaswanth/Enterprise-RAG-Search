import fitz
import os


PDF_PATH = "data/documents/Enterprise_RAG_Company_Documents.pdf"


def load_pdf(path):

    document = fitz.open(path)

    text = ""

    for page_number, page in enumerate(document):
        page_text = page.get_text()

        text += page_text + "\n"

    document.close()

    return text


if __name__ == "__main__":

    print("Loading PDF...")

    pdf_text = load_pdf(PDF_PATH)

    print("PDF loaded successfully!")

    print("\nTotal characters:")
    print(len(pdf_text))

    print("\nFirst 1000 characters:")
    print("--------------------------------")

    print(pdf_text[:1000])