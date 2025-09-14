import yt_dlp
from yt_dlp.utils import DownloadError
from datetime import datetime
import whisper
from langdetect import detect
from googletrans import Translator
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def timestamped_filename(base, ext):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{ts}.{ext}"

# Step 1: Download video from YouTube
def download_video(youtube_url):
    """
    Downloads the best video+audio into output/video.mp4.
    Falls back to the single best file if the merge spec isn't available.
    """
    output_path = os.path.join(OUTPUT_DIR, "video.mp4").replace("\\", "/")

    ydl_opts = {
        "outtmpl": output_path,
        # 1. Try merging best video + best audio
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

    except DownloadError as e:
        # 2. Fallback to a single best‐quality file if merging fails
        print(f"[yt-dlp] merge-spec failed: {e}\nFalling back to best single file…")
        ydl_opts["format"] = "best"
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

    return output_path
# def download_video(youtube_url, filename="video.mp4"):
    yt = YouTube(youtube_url)
    video_stream = yt.streams.get_highest_resolution().order_by('resolution').desc().first()
    
    # Download to the correct folder
    video_stream.download(output_path=OUTPUT_DIR, filename=filename)
    
    full_path = os.path.join(OUTPUT_DIR, filename)
    print(f"Downloaded video to {full_path}")
    return full_path

# Step 2: Transcribe audio using Whisper, separated by timestamp segments
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, verbose=True)
    print("Transcription complete.")
    return result["segments"]

# Step 3: Detect language
def detect_language(text):
    lang = detect(text)
    print(f"Detected language: {lang}")
    return lang

# Step 4: Translate each segment to English
def translate_segments(segments, src_lang):
    translator = Translator()
    for segment in segments:
        translated = translator.translate(segment["text"], src=src_lang, dest='en')
        segment["text"] = translated.text
    print("All segments translated to English.")
    return segments

# Step 5: Generate SRT file
def generate_srt(transcription_segments, filename="captions.srt"):
    srt_path = os.path.join(OUTPUT_DIR, filename)

    def format_timestamp(seconds):
        hrs, secs = divmod(seconds, 3600)
        mins, secs = divmod(secs, 60)
        millis = int((secs - int(secs)) * 1000)
        return f"{int(hrs):02}:{int(mins):02}:{int(secs):02},{millis:03}"

    with open(srt_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription_segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

    print(f"SRT file saved to {srt_path}")
    return srt_path

# Step 6: Add subtitles to video using ffmpeg
def add_subtitles_to_video(video_path, srt_path, filename="captioned_video.mp4"):
    import subprocess

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Normalize paths for FFmpeg (use forward slashes)
    srt_path_ffmpeg = srt_path.replace("\\", "/")
    output_path = os.path.join(OUTPUT_DIR, filename).replace("\\", "/")

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles='{srt_path_ffmpeg}'",
        "-c:a", "copy",
        output_path
    ]

    # Run as a shell command so FFmpeg parses the filter correctly
    subprocess.run(" ".join(cmd), shell=True, check=True)
    print(f"Captioned video saved to {output_path}")
    return output_path


# Main function
def process_youtube_video(youtube_url):
    video_path = download_video(youtube_url)
    segments = transcribe_audio(video_path)

    full_text = " ".join([seg["text"] for seg in segments])
    src_lang = detect_language(full_text)
    translated_segments = translate_segments(segments, src_lang)

    srt_path = generate_srt(translated_segments)
    captioned_video = add_subtitles_to_video(video_path, srt_path)

    print("\n✅ All done! Your files are saved in the 'output' folder.")

# Replace with your desired YouTube video URL
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=sqcess88xCo"
    process_youtube_video(video_url)
