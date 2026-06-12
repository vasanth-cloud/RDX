from services.vector_store import (
    embedding_model,
    collection
)


def store_documents(documents):

    for doc in documents:

        embedding = embedding_model.encode(
            doc["text"]
        ).tolist()

        collection.add(
            ids=[doc["id"]],
            documents=[doc["text"]],
            embeddings=[embedding],
            metadatas=[
                {
                    "source": doc["source"]
                }
            ]
        )