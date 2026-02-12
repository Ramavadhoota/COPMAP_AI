import os
from typing import Any, Dict, List

import chromadb
from sentence_transformers import SentenceTransformer

from ..config import settings


class RagService:
    def __init__(self):
        os.makedirs(settings.CHROMA_DIR, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DIR
        )

        # Explicit embedding model (recommended for Chroma 1.x)
        self.embedder = SentenceTransformer(settings.EMBEDDING_MODEL)

        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION
        )

    def _embed(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.encode(
            texts,
            normalize_embeddings=True
        ).tolist()

    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        # Chroma metadata values must be scalar types (or None), not nested objects.
        clean: Dict[str, Any] = {}
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                clean[key] = value
            else:
                clean[key] = str(value)
        return clean

    def ingest(self, doc_id: str, content: str, metadata: Dict[str, Any]):
        embeddings = self._embed([content])
        clean_metadata = self._sanitize_metadata(metadata)

        self.collection.upsert(
            ids=[doc_id],
            documents=[content],
            metadatas=[clean_metadata],
            embeddings=embeddings,
        )

    def query(
        self,
        query_text: str,
        k: int = 4,
        where: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:

        query_embedding = self._embed([query_text])
        where_filter = where or None

        res = self.collection.query(
            query_embeddings=query_embedding,
            n_results=k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]

        return [
            {
                "content": d,
                "metadata": m,
                "distance": dist
            }
            for d, m, dist in zip(docs, metas, dists)
        ]


rag_service = RagService()
