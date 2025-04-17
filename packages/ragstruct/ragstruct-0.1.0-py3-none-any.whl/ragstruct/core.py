import os
import json
import numpy as np
from typing import List, Union, Optional, Callable


class ragstruct:
    def __init__(
        self,
        embedding_model,
        llm_model: Optional[Callable] = None,
        document: Optional[Union[str, dict]] = None,
        from_json: bool = True,
    ):
        """
        :param embedding_model: Any embedding model with `embed_documents()` and `embed_query()`
        :param llm_model: Optional LLM callable to parse raw text into structured JSON
        :param document: A JSON/dict or plain text document
        :param from_json: True if document is JSON, False if it's raw text
        """
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.kv_pairs = []
        self.keys = []
        self.values = []
        self.embeddings = []

        if document:
            self.load_document(document, from_json)

    def load_document(self, document: Union[str, dict], from_json: bool = True):
        if not from_json and self.llm_model:
            document = self._structure_text(document)
        if isinstance(document, str) and from_json:
            document = json.loads(document)
        self.kv_pairs = self._extract_kv_pairs(document)
        self.keys = [k for k, _ in self.kv_pairs]
        self.values = [v for _, v in self.kv_pairs]
        self.embeddings = self.embedding_model.embed_documents(self.keys)

    def _structure_text(self, text: str) -> dict:
        prompt = f"""Convert the following document into structured JSON format for use in a semantic search system:\n\n{text}"""
        return json.loads(self.llm_model.invoke(prompt))

    def _extract_kv_pairs(self, obj, parent_key=''):
        items = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                full_key = f"{parent_key}.{k}" if parent_key else k
                items.extend(self._extract_kv_pairs(v, full_key))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                full_key = f"{parent_key}[{i}]"
                items.extend(self._extract_kv_pairs(v, full_key))
        else:
            items.append((parent_key, str(obj)))
        return items

    def _cosine_sim(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def retrieve(self, query: str, threshold=0.5, top_k=3) -> List[str]:
        query_emb = self.embedding_model.embed_query(query)
        scored = []

        for key, val, emb in zip(self.keys, self.values, self.embeddings):
            sim = self._cosine_sim(query_emb, emb)
            if sim >= threshold:
                scored.append((key, val, sim))

        scored.sort(key=lambda x: x[2], reverse=True)
        return [(key, val) for key, val, _ in scored[:top_k]]
