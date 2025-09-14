from pytubefix import YouTube
import whisper
from langdetect import detect
from googletrans import Translator
import os

# Step 1: Download video from YouTube
def download_video(youtube_url, output_path="video.mp4"):
    yt = YouTube(youtube_url)
    video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    video_stream.download(filename=output_path)
    print(f"Downloaded video to {output_path}")
    return output_path

# Step 2: Transcribe audio using Whisper
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

# Step 4: Translate to English
# def translate_to_english(text, src_lang):
#     translator = Translator()
#     translated = translator.translate(text, src=src_lang, dest='en')
#     print("Translation complete.")
#     return translated.text

# Step 4: Translate each segment to English
def translate_segments(segments, src_lang):
    translator = Translator()
    for segment in segments:
        translated = translator.translate(segment["text"], src=src_lang, dest='en')
        segment["text"] = translated.text
    print("All segments translated to English.")
    return segments

# Step 5: Generate SRT file
def generate_srt(transcription_segments, srt_path="captions.srt"):
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
def add_subtitles_to_video(video_path, srt_path, output_path="captioned_video.mp4"):
    import subprocess
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}",
        "-c:a", "copy",
        output_path
    ]
    subprocess.run(cmd, check=True)
    print(f"Captioned video saved to {output_path}")
    return output_path


# Main function
def process_youtube_video(youtube_url):
    video_path = download_video(youtube_url)
    segments = transcribe_audio(video_path)

    # Combine all text to detect language
    full_text = " ".join([seg["text"] for seg in segments])
    src_lang = detect_language(full_text)

    # Translate segments
    translated_segments = translate_segments(segments, src_lang)

    srt_path = generate_srt(translated_segments)
    captioned_video = add_subtitles_to_video(video_path, srt_path)

    print("\n✅ All done! Your video now has English captions.")

# Replace with your desired YouTube video URL
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=sqcess88xCo"
    process_youtube_video(video_url)
