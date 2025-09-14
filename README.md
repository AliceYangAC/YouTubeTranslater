# YouTubeTranslater

A Python tool that downloads a YouTube video, transcribes its audio with OpenAI Whisper, auto-detects and translates the transcript into English, generates an SRT subtitle file, and adds captions back into the video.

---

## Features

- Download any public YouTube video
- Transcribe speech using OpenAI Whisper  
- Auto-detect source language and translate to English  
- Generate timestamped `.srt` subtitle files  
- Burn captions into a new MP4 video via FFmpeg  
- Clean command-line interface with clear progress output  

---

## Prerequisites

- Python 3.10+ (recommended)  
- FFmpeg installed and on your system PATH 
- Internet access for YouTube download and translation  

---

## Installation

1. Clone this repository  
   ```bash
   git clone https://github.com/AliceYangAC/YouTubeTranslater.git
   cd YouTubeTranslater
   ```

2. Create and activate a Python 3.10+ virtual environment  
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .\.venv\Scripts\activate       # Windows PowerShell
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

4. Verify FFmpeg is available; if just installed and not visible, reboot your editor or terminal.
   ```bash
   ffmpeg -version
   ```

---

## Usage

Run the main script and pass a YouTube URL to line 139 at `[VIDEO ID]`:

```bash
python translator.py
```

By default, the downloaded video is saved as `output/video.mp4`. After processing, you’ll find:

- `output/video.mp4` (downloaded source)  
- `output/captions.srt` (generated subtitles)  
- `output/captioned_video.mp4` (final video with burned-in captions)  

---

## Configuration

- To change the Whisper model (e.g., from `base` to `small`), edit the `transcribe_audio()` call in `translator.py`  
- Adjust FFmpeg parameters in `ensure_wav()` or subtitle burn-in section for custom sample rates or styling  
- Modify output folder or naming conventions by updating the `OUTPUT_DIR` and `timestamped_filename()` function  

---

## Troubleshooting

- HTTP 400 errors on download  
  - Ensure URLs are stripped of extra whitespace  
- Whisper build failures on Python >3.10  
  - Use the GitHub install: `git+https://github.com/openai/whisper.git`  
  - Downgrade your venv to Python 3.10 if needed  
- FFmpeg “no audio stream” errors  
  - Confirm merged audio/video by running `ffprobe output/video.mp4`  
  - Use the `ensure_wav()` helper to extract a clean mono WAV at 16 kHz  

---

## Future Plans

1. Interactive Web or Desktop GUI

    - Local upload support for video files and URL input

    - Real-time progress logs and error reporting panel

2. Multi-Language Output

    - Let users choose target translation languages beyond English

    - Generate separate SRT files per language or a single multi-language SRT, incl. dual-language captions

3. Export & Sharing Options

    - Export transcripts as plain text, JSON, or Markdown with timestamps

    - Auto-generate YouTube-friendly captions package (.srt + transcript)

    - One-click upload of caption files back to YouTube via YouTube Data API

4. AI-Powered Summaries & Highlights

    - Automatically summarize long videos into bullet-point notes

    - Sentiment or topic analysis across transcript sections

5. Packaging & Distribution

    - Turn the project into a pip-installable package or standalone executable

    - Provide Docker images for easy deployment in CI/CD pipelines

    - Offer a cloud-hosted service with simple REST API endpoints

---

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.