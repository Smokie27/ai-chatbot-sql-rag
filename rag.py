import os
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings



# LOAD LLM & EMBEDDINGS

llm = OllamaLLM(model="llama3")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


VECTOR_DB_PATH = "vector_store"

# BUILD VECTOR DATABASE

def build_vector_db():
    docs = []

    if not os.path.exists("documents"):
        raise FileNotFoundError("documents folder not found")

    for file in os.listdir("documents"):
        if file.lower().endswith(".pdf"):
            loader = PyPDFLoader(os.path.join("documents", file))
            docs.extend(loader.load())

    if len(docs) == 0:
        raise ValueError("No PDF documents found in documents folder")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTOR_DB_PATH)

    print(f"Vector DB built successfully with {len(chunks)} chunks.")

# LOAD VECTOR DATABASE

def load_vector_db():
    if not os.path.exists(VECTOR_DB_PATH):
        raise FileNotFoundError("Vector DB not found. Run build_vector_db() first.")

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

# ASK PDF DOCUMENTS (RAG)

def ask_pdf(question):
    db = load_vector_db()
    docs = db.similarity_search(question, k=4)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a financial analyst.

Use ONLY the context below to answer the question.
If the answer is not present in the context, say "Not found in documents".

Context:
{context}

Question:
{question}

Answer:
"""
    return llm.invoke(prompt)

def get_pdf_context(question):
    db = load_vector_db()
    docs = db.similarity_search(question, k=4)
    return "\n\n".join([d.page_content for d in docs])


