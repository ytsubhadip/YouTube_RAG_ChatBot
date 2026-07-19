from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

from src.Youtube_extractor import extract_video_text
from src.TextSpllitor import prepare_transcript_for_vectorstore

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_OLLAMA_MODEL = "llama3.1:8b"
DEFAULT_K = 4

PROMPT_TEMPLATE = """You are a helpful assistant grounded in the supplied transcript context.
Use the transcript chunks to answer the user's question.
If the answer is not explicitly present in the context, say that the transcript does not contain enough information.

Context:
{context}

Question:
{question}

Answer:
"""


def extract_video_id(video_url: str) -> str:
    """Extract the 11-character YouTube video ID from a standard URL."""
    if "youtu.be/" in video_url:
        video_id = video_url.split("youtu.be/")[-1].split("?")[0].split("&")[0]
    elif "v=" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        video_id = video_url.strip()

    return video_id[:11]


def get_vectorstore_dir(video_id: str, base_dir: str = "vectorstores") -> Path:
    return Path(base_dir) / video_id


def get_embedding_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=DEFAULT_EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore_for_video(video_url: str, base_dir: str = "vectorstores") -> Path:
    """Fetch transcript, split it into chunks, embed them and save one FAISS index per video ID."""
    video_id = extract_video_id(video_url)
    transcript_text = extract_video_text(video_url)
    if not transcript_text:
        raise ValueError(f"Unable to extract transcript text for video {video_id}")

    chunks = prepare_transcript_for_vectorstore(transcript_text, video_id)
    embeddings = get_embedding_model()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    index_dir = get_vectorstore_dir(video_id, base_dir=base_dir)
    index_dir.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_dir))

    return index_dir


def load_vectorstore(video_id: str, base_dir: str = "vectorstores") -> FAISS:
    index_dir = get_vectorstore_dir(video_id, base_dir=base_dir)
    if not index_dir.exists():
        raise FileNotFoundError(
            f"No FAISS vector store found for {video_id}. Run build_vectorstore_for_video() first."
        )

    embeddings = get_embedding_model()
    return FAISS.load_local(
        str(index_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def answer_question(video_url: str, question: str, base_dir: str = "vectorstores") -> str:
    """Retrieve from the per-video index and answer using a local Ollama model."""
    video_id = extract_video_id(video_url)
    vectorstore = load_vectorstore(video_id, base_dir=base_dir)

    retriever = vectorstore.as_retriever(search_kwargs={"k": DEFAULT_K})
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE,
    )
    llm = ChatOllama(model=DEFAULT_OLLAMA_MODEL, temperature=0)

    def _format_docs(docs: list[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    runnable = (
        {
            "context": retriever | _format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    return runnable.invoke(question).content
