import json
import re
from typing import Any, List, Dict
from dataclasses import dataclass

@dataclass
class Structurer:
    llm: Any                      # Any LLM that supports `.invoke(prompt)`
    chunk_size: int = 800        # Size per chunk (approx. in chars)
    chunk_overlap: int = 100     # Overlap between chunks

    def _chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks, start = [], 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            start = end - self.chunk_overlap  # slide back a bit for context
        return chunks

    def _structure_chunk(self, chunk: str) -> Dict:
        system_instruction = (
            "You are an AI that converts unstructured text into structured JSON.\n"
            "Structure this paragraph into meaningful fields like 'topic', 'details', 'entities', 'intent', etc., "
            "if applicable. Use clean keys and clear value descriptions.\n\n"
        )

        prompt = f"{system_instruction}Text:\n\"\"\"\n{chunk}\n\"\"\""
        result = self.llm.invoke(prompt)

        try:
            structured = json.loads(result)
        except Exception:
            # Attempt to extract JSON from messy LLM responses
            match = re.search(r"\{.*\}", result, re.DOTALL)
            if match:
                try:
                    structured = json.loads(match.group())
                except Exception:
                    structured = {"raw_chunk": chunk, "parsed": result.strip()}
            else:
                structured = {"raw_chunk": chunk, "parsed": result.strip()}
        return structured

    def structure_document(self, text: str) -> List[Dict]:
        chunks = self._chunk_text(text)
        structured_chunks = []
        for i, chunk in enumerate(chunks):
            print(f"🧩 Structuring chunk {i+1}/{len(chunks)}...")
            structured = self._structure_chunk(chunk)
            structured_chunks.append(structured)
        return structured_chunks
