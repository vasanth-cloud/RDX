from rank_bm25 import BM25Okapi
import re


class BM25Store:

    def __init__(self):

        self.documents = []
        self.bm25 = None

    def tokenize(self, text):

        return re.findall(
            r"\w+",
            text.lower()
        )

    def build(self, documents):

        self.documents = documents

        tokenized_docs = [
            self.tokenize(doc["text"])
            for doc in documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_docs
        )

        print(
            f"BM25 initialized with {len(documents)} documents"
        )

    def search(self, query, top_k=5):

        if self.bm25 is None:

            raise Exception(
                "BM25 not initialized"
            )

        scores = self.bm25.get_scores(
            self.tokenize(query)
        )

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, _
            in ranked[:top_k]
        ]