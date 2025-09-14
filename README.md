# YouTubeTranslater

A Python-based tool with a GUI to allow the user to download a YouTube video, transcribe its audio with OpenAI Whisper, auto-detect the language of and translate the transcript into another chosen language, generates an SRT subtitle file, and adds the SRT subtitles back into the video.

---

## Features

- Accept Youtube URL input and limited language selection through Tkinter GUI
- Download any public YouTube video
- Transcribe speech using OpenAI Whisper  
- Auto-detect source language to translate from
- Generate timestamped `.srt` subtitle files  
- Burn captions into a new MP4 video via FFmpeg  
- View event pipeline logs on GUI

---

## Prerequisites

- Python 3.10+ (recommended)  
- FFmpeg installed and on your system PATH 
- Internet access for YouTube download and translation  

---

## Installation

1. Clone this repository  
   ```bash
   git clone https://github.com/AliceYangAC/WhisperSRTube.git
   cd WhisperSRTube
   ```

2. Create and activate a Python 3.10+ virtual environment  
   ```bash
   py -m venv .venv
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

1. Run the `translator_gui.py` script to launch the GUI app:

```bash
py translator.py
```

2. Input a YouTube URL and select a target language to translate the video to from the drop down list.
3. Press `Start` and wait for the pipeline to finish.
4. View output video and/or SRT subtitles in the untraced `output` folder on your local machine.

---

## Configuration

- To change the Whisper model (e.g., from `base` to `small`), edit the `transcribe_audio()` call in `translator.py`  
- Modify output folder or naming conventions by updating the `OUTPUT_DIR` and `timestamped_filename()` function in the `translator.py` script.
- To add more languages, add the language and its respective language code in the `LANGUAGES` dict in the `translator_gui.py` script.

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

1. <del>Interactive Web or Desktop GUI</del>

2. <del>Multi-Language Output</del

    - <del>Let users choose target translation languages beyond English</del>

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