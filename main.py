import eel
import os
from pathlib import Path
from tkinter import filedialog, Tk
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor

eel.init("web")

languages = {
    "Auto Detect": "auto",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Dutch": "nl",
    "Polish": "pl",
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
}

@eel.expose
def get_languages():
    return list(languages.keys())

@eel.expose
def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    root.destroy()
    return file_path if file_path else ""

@eel.expose
def translate_file(file_path, src_lang_key):
    if not os.path.exists(file_path):
        return f"Error: File not found.\n{file_path}"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception as e:
        return f"Error reading file: {e}"

    src_lang = languages.get(src_lang_key, "auto")
    translator = GoogleTranslator(source=src_lang, target="en")

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(translator.translate, line) if line.strip() else None
            for line in lines
        ]
        for future, line in zip(futures, lines):
            if future is not None:
                try:
                    translated = future.result()
                except Exception as e:
                    translated = f"[Translation failed: {e}]"
            else:
                translated = ""
            results.append(translated)

    # Clean duplicates & extra blank lines
    cleaned_results = []
    last_line = None
    last_was_empty = False

    for line in results:
        if not line.strip():
            if not last_was_empty:
                cleaned_results.append("")
                last_was_empty = True
            continue
        last_was_empty = False
        if line == last_line:
            continue
        cleaned_results.append(line)
        last_line = line

    formatted = []
    display_idx = 1
    for line in cleaned_results:
        if line.strip():
            formatted.append(f"{display_idx}. {line}")
            display_idx += 1
        else:
            formatted.append("")

    return "\n".join(formatted)

if __name__ == "__main__":
    eel.start("index.html", size=(900, 700))
