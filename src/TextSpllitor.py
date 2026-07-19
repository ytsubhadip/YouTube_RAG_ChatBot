from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:
    from langchain_core.documents import Document
    from langchain_core.text_splitter import RecursiveCharacterTextSplitter
except ModuleNotFoundError:
    @dataclass
    class Document:
        page_content: str
        metadata: dict[str, str]
        id: str = ""

    class RecursiveCharacterTextSplitter:
        def __init__(
            self,
            chunk_size: int = 1000,
            chunk_overlap: int = 200,
            length_function: Any = len,
            separators: list[str] | None = None,
        ):
            self.chunk_size = chunk_size
            self.chunk_overlap = chunk_overlap
            self.length_function = length_function
            self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

        def create_documents(self, texts: list[str], metadatas: list[dict[str, str]] | None = None):
            docs: list[Document] = []
            metadatas = metadatas or [{} for _ in texts]

            for text, metadata in zip(texts, metadatas):
                chunks = self._chunk_text(text)
                for index, chunk in enumerate(chunks):
                    chunk_metadata = dict(metadata)
                    chunk_metadata["chunk_index"] = str(index)
                    docs.append(
                        Document(
                            id=f"{metadata.get('video_id', 'doc')}-{index}",
                            page_content=chunk,
                            metadata=chunk_metadata,
                        )
                    )

            return docs

        def _chunk_text(self, text: str) -> list[str]:
            text = text.strip()
            if not text:
                return []

            chunks: list[str] = []
            start = 0
            while start < len(text):
                end = min(start + self.chunk_size, len(text))
                chunk = text[start:end]
                chunks.append(chunk.strip())
                if end == len(text):
                    break
                start = max(end - self.chunk_overlap, start + 1)

            return [chunk for chunk in chunks if chunk]


def prepare_transcript_for_vectorstore(transcript_text: str, video_id: str) -> list[Document]:
    """
    Split a YouTube transcript into overlapping chunks for vector ingestion.
    Falls back to a lightweight local implementation if LangChain is unavailable.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = text_splitter.create_documents(
        texts=[transcript_text],
        metadatas=[
            {
                "video_id": video_id,
                "source": f"https://youtube.com/watch?v={video_id}",
            }
        ],
    )

    return chunks
