# translator_gui.py

import threading
import tkinter as tk
from tkinter import ttk, messagebox

import translator        # translator.py
from langdetect import detect
from googletrans import Translator as GoogleTranslator

# A small set of language names & codes; extend this later
LANGUAGES = {
    "English":     "en",
    "Spanish":     "es",
    "French":      "fr",
    "German":      "de",
    "Chinese":     "zh-cn",
    "Japanese":    "ja",
    "Korean":      "ko",
    "Portuguese":  "pt",
    "Russian":     "ru",
}


class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WhisperSRTube: YouTube Translator & Subtitler")
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _build_ui(self):
        frm = ttk.Frame(self, padding=10)
        frm.grid(sticky="ew")
        frm.columnconfigure(1, weight=1)

        # YouTube URL entry
        ttk.Label(frm, text="YouTube URL:").grid(row=0, column=0, sticky="w")
        self.url_entry = ttk.Entry(frm)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=(5,0))

        # Language dropdown
        ttk.Label(frm, text="Translate to:").grid(row=1, column=0, sticky="w", pady=(5,0))
        self.lang_var = tk.StringVar(value="English")
        ttk.OptionMenu(frm, self.lang_var, "English", *LANGUAGES.keys())\
            .grid(row=1, column=1, sticky="w", padx=(5,0), pady=(5,0))

        # Start button
        self.start_btn = ttk.Button(frm, text="Start", command=self._on_start)
        self.start_btn.grid(row=2, column=0, columnspan=2, pady=(10,0))

        # Log box
        self.log = tk.Text(self, wrap="word", height=15, state="disabled")
        self.log.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.rowconfigure(3, weight=1)

        sb = ttk.Scrollbar(self, command=self.log.yview)
        sb.grid(row=3, column=1, sticky="ns")
        self.log.config(yscrollcommand=sb.set)

    def _log(self, msg):
        self.log.config(state="normal")
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.log.config(state="disabled")
        self.update_idletasks()

    def _on_start(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a YouTube URL.")
            return

        target_name = self.lang_var.get()
        target_code = LANGUAGES[target_name]

        # Disable UI
        self.start_btn.config(state="disabled")
        self._log(f"→ Starting pipeline for {url} → {target_name}")

        threading.Thread(
            target=self._run_pipeline,
            args=(url, target_code),
            daemon=True
        ).start()

    def _run_pipeline(self, url, target_code):
        try:
            # 1) Download
            self._log("Downloading video…")
            video_path = translator.download_video(url)
            self._log(f"Downloaded to {video_path}")

            # 2) Transcribe
            self._log("Transcribing audio…")
            segments = translator.transcribe_audio(video_path)
            self._log(f"Got {len(segments)} segments")

            # 3) Auto-detect source language
            full = " ".join(seg["text"] for seg in segments)
            src = detect(full)
            self._log(f"Detected source language: {src}")

            # 4) Translate
            self._log(f"Translating segments to '{target_code}'…")
            gt = GoogleTranslator()
            for seg in segments:
                tr = gt.translate(seg["text"], src=src, dest=target_code)
                seg["text"] = tr.text
            self._log("Translation complete")

            # 5) Write SRT
            srt = translator.generate_srt(segments, filename=f"captions_{target_code}.srt")
            self._log(f"SRT saved to {srt}")

            # 6) Add subtitles
            out_vid = translator.add_subtitles_to_video(
                video_path, srt, filename=f"captioned_{target_code}.mp4"
            )
            self._log(f"Captioned video → {out_vid}")

            self._log("✅ Video finished!")
            messagebox.showinfo("Success", f"Captioned video:\n{out_vid}")

        except Exception as e:
            self._log(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))

        finally:
            self.start_btn.config(state="normal")


if __name__ == "__main__":
    app = Gui()
    app.geometry("700x450")
    app.mainloop()
