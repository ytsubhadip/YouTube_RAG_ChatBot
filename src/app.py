# Import the function from your custom module
from Youtube_extractor import extract_video_text

# Example YouTube URL
url = "https://youtu.be/zVHOF-Mc_xU?si=drF0yhDq6EqHqs1L"

# Fetch the text (it will automatically route to the right method)
video_text = extract_video_text(url)

print("\n--- Final Extracted Text ---")
print(video_text)