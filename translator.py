import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from pathlib import Path
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor
import threading

ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("800x600")
root.title("Translate TXT File")

# --- Language selection ---
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
lang_var = ctk.StringVar(value="Auto Detect")
lang_menu = ctk.CTkOptionMenu(root, values=list(languages.keys()), variable=lang_var)
lang_menu.pack(padx=10, pady=5)

path_label = ctk.CTkLabel(root, text="No file loaded")
path_label.pack(padx=10, pady=5)

# --- Translate function ---
def translate_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        path_label.configure(text=f"Loaded: {file_path}")
    except Exception as e:
        path_label.configure(text=f"Error: {e}")
        return

    out_win = ctk.CTkToplevel(root)
    out_win.title(f"Translated - {Path(file_path).name}")

    # Use standard Tk Text widget for efficiency
    text_box = tk.Text(out_win, wrap="word", spacing1=1, spacing2=1, spacing3=1)
    text_box.pack(fill="both", expand=True, padx=10, pady=10)
    text_box.insert("end", "Translating...\n")
    text_box.update()

    src_lang = languages[lang_var.get()]
    translator = GoogleTranslator(source=src_lang, target="en")

    def worker():
        results = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(translator.translate, line) if line.strip() else None for line in lines]
            for future, line in zip(futures, lines):
                if future is not None:
                    try:
                        translated = future.result()
                    except Exception as e:
                        translated = f"[Translation failed: {e}]"
                else:
                    translated = ""
                results.append(translated)

        # --- Collapse consecutive empty lines and remove exact duplicates ---
        cleaned_results = []
        last_line = None
        last_was_empty = False

        for line in results:
            if not line.strip():  # empty line
                if not last_was_empty:
                    cleaned_results.append("")
                    last_was_empty = True
                continue
            last_was_empty = False

            if line == last_line:
                continue  # skip exact duplicates

            cleaned_results.append(line)
            last_line = line

        # --- Insert text into textbox ---
        text_box.configure(state="normal")
        text_box.delete("1.0", "end")
        display_idx = 1

        for line in cleaned_results:
            if not line.strip():
                text_box.insert("end", "\n")
                continue
            start_index = text_box.index("end-1c")
            text_box.insert("end", f"{display_idx}. {line}\n")
            end_index = text_box.index("end-1c")
            text_box.tag_add(f"line{display_idx}", start_index, end_index)
            text_box.tag_config(f"line{display_idx}", justify="center")
            display_idx += 1

        text_box.configure(state="disabled")

    threading.Thread(target=worker, daemon=True).start()

# --- File selection button ---
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        translate_file(file_path)

select_button = ctk.CTkButton(root, text="Select TXT File", command=select_file)
select_button.pack(padx=10, pady=5)


root.mainloop()
