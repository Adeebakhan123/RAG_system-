from src.ingestion.loader import load_pdf
from src.ingestion.splitter import split_documents
from src.embeddings.embedding_manager import EmbeddingManager
from src.vectorstore.vector_store import VectorStore
from src.retrieval.retriever import RAGRetriever

def run_pipeline():

    # 1. Load
    documents = load_pdf("data\raw\BTP _report_22AE10001.pdf")

    # 2. Split
    chunks = split_documents(documents)

    # 3. Embedding
    embedder = EmbeddingManager()
    texts = [doc.page_content for doc in chunks]
    embeddings = embedder.generate_embeddings(texts)

    # 4. Store
    vectorstore = VectorStore()
    vectorstore.add_documents(chunks, embeddings)

    # 5. Retrieve
    retriever = RAGRetriever(vectorstore, embedder)

    results = retriever.retrieve("Fundamentals of Truss Structures")

    print(results)