import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
from faster_whisper import WhisperModel


def _get_fast_transcript(video_id: str) -> str | None:
    """Attempt to get the transcript using YouTube's built-in captions."""
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=("en", "hi"))
        return " ".join([item.text for item in transcript])
    except Exception as e:
        print(f"Fast transcript failed: {e}")
        return None

def _get_whisper_transcript(video_url):
    """Download audio and transcribe it using faster-whisper."""
    print("Falling back to AI audio transcription. This may take a moment...")
    
    # Set up audio download options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio_temp.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True, # Suppress yt-dlp terminal output
    }
    
    # Download audio
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    
    # Transcribe audio
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe("audio_temp.mp3", beam_size=5,language="en", vad_filter=True)
    full_text = " ".join([segment.text for segment in segments])
    
    # Clean up the downloaded file
    if os.path.exists("audio_temp.mp3"):
        os.remove("audio_temp.mp3")
        
    return full_text

def extract_video_text(video_url: str) -> str | None:
    """
    Main function to extract text from a YouTube URL or video ID.
    Tries the fast API first, falls back to Whisper AI if needed.
    """
    video_id_match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", video_url)
    if video_id_match:
        video_id = video_id_match.group(1)
    elif len(video_url) >= 11 and re.fullmatch(r"[A-Za-z0-9_-]{11}", video_url):
        video_id = video_url
    else:
        video_id = video_url.split("v=")[-1].split("&")[0][:11]

    print(f"Processing video: {video_id}")

    text = _get_fast_transcript(video_id)
    if text is None:
        text = _get_whisper_transcript(video_url)

    return text