class RAGRetriever:
  def __init__(self, vectorstore:VectorStore, embedding_manager:EmbeddingManager):
    self.vectorstore = vectorstore # Corrected assignment
    self.embedding_manager = embedding_manager # Corrected assignment

  def retrieve(self, query: str, top_k: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
      """
      Retrieve relevant documents for a query

      Args:
          query: The search query
          top_k: Number of top results to return
          score_threshold: Minimum similarity score threshold

      Returns:
          List of dictionaries containing retrieved documents and metadata
      """
      print(f"Retrieving documents for query: '{query}'")
      print(f"Top K: {top_k}, Score threshold: {score_threshold}")

      # Generate query embedding
      query_embedding = self.embedding_manager.generate_embeddings([query])[0]

      try:

          results = self.vectorstore.collection.query( # Corrected from self.vector_store to self.vectorstore
              query_embeddings=[query_embedding.tolist()],
              n_results=top_k
          )

          # Process results
          retrieved_docs = []

          if results['documents'] and results['documents'][0]:
              documents = results['documents'][0]
              metadatas = results['metadatas'][0]
              distances = results['distances'][0]
              ids = results['ids'][0]

              for i, (doc_id, document, metadata, distance) in enumerate(zip(ids, documents, metadatas, distances)):
                # Convert distance to similarity score (ChromaDB uses cosine distance)
                similarity_score = 1 - distance

                if similarity_score >= score_threshold:
                    retrieved_docs.append({
                        'id': doc_id,
                        'content': document,
                        'metadata': metadata,
                        'similarity_score': similarity_score,
                        'distance': distance,
                        'rank': i + 1
                    })

              print(f"Retrieved {len(retrieved_docs)} documents (after filtering)")
          else:
              print("No documents found")

          return retrieved_docs

      except Exception as e:
          print(f"Error during retrieval: {e}")
          return[]
##rag_retriever= RAGRetriever(vectorstore,embedding_manager)