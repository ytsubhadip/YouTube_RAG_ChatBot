from __future__ import annotations

import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.rag_pipeline import answer_question, build_vectorstore_for_video

VIDEO_URL = input("Enter the YouTube video URL: ")
QUESTION = input("Enter your question: ")


if __name__ == "__main__":
    try:
        build_vectorstore_for_video(VIDEO_URL)
        answer = answer_question(VIDEO_URL, QUESTION)
        print("\n--- RAG Answer ---")
        print(answer)
    except Exception as exc:
        print(f"Pipeline failed: {exc}")