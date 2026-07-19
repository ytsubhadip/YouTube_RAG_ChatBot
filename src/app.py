from __future__ import annotations

from src.rag_pipeline import answer_question, build_vectorstore_for_video

VIDEO_URL = "https://youtu.be/zVHOF-Mc_xU?si=drF0yhDq6EqHqs1L"
QUESTION = "Who is the principal of ILEAD Kolkata?"


if __name__ == "__main__":
    try:
        build_vectorstore_for_video(VIDEO_URL)
        answer = answer_question(VIDEO_URL, QUESTION)
        print("\n--- RAG Answer ---")
        print(answer)
    except Exception as exc:
        print(f"Pipeline failed: {exc}")