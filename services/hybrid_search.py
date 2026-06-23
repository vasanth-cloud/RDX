from services.vector_store import (
    collection,
    embedding_model
)


class HybridSearch:

    def __init__(self, bm25_store):

        self.bm25_store = bm25_store

    def search(self, query, top_k=5):

        # BM25 Results
        bm25_results = self.bm25_store.search(
            query,
            top_k=top_k
        )

        # Chroma Results
        query_embedding = (
            embedding_model.encode(query)
            .tolist()
        )

        vector_results = collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k
        )

        chroma_docs = []

        docs = vector_results["documents"][0]
        metas = vector_results["metadatas"][0]

        for i in range(len(docs)):

            chroma_docs.append(
                {
                    "id": str(i),
                    "text": docs[i],
                    "source": metas[i]["source"]
                }
            )

        # Merge Results
        final_results = []
        seen = set()

        # Chroma first (better semantic relevance)
        for doc in chroma_docs:

            key = doc["text"][:100]

            if key not in seen:

                final_results.append(doc)
                seen.add(key)

        # BM25 next
        for doc in bm25_results:

            key = doc["text"][:100]

            if key not in seen:

                final_results.append(doc)
                seen.add(key)

        # Debug Output
        print("\n========== HYBRID SEARCH RESULTS ==========")

        for i, doc in enumerate(final_results, start=1):

            print(f"\nRESULT {i}")
            print("SOURCE:", doc["source"])
            print(doc["text"][:500])

        print("\n===========================================")

        return final_results[:top_k]