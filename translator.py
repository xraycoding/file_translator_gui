from tkinter import StringVar, TOP
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from pathlib import Path
from googletrans import Translator
import asyncio



class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

ctk.set_appearance_mode("dark")

def get_text(event):
    file_path = event.data.strip('{}')  # Remove curly braces if present
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            file_name = Path(file_path).name
        pathLabel.configure(text=f"File loaded:\n{file_path}")
        # Show file content in a new window or print to console
        translate_content(file_content,file_name)
    except Exception as e:
        pathLabel.configure(text=f"Error: {e}")

def translate_content(content,name):
    translator = Translator()
    try:
        if not content:
            show_file_content("", name)
            return
        result = translator.translate(content, dest='en')
        # handle async coroutine returned by some googletrans builds
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)
        # googletrans may return a single object or a list for long input; handle both
        if isinstance(result, list):
            result_text = "\n\n".join(t.text for t in result)
        else:
            result_text = result.text
        show_file_content(result_text, name)
    except Exception as e:
        pathLabel.configure(text=f"Translation error: {e}")

def show_file_content(content,name):
    # Display the file content in a new CTk window
    content_window = ctk.CTkToplevel(root)
    content_window.title(name)
    text_box = ctk.CTkTextbox(content_window, width=1280, height=720)
    text_box.pack(padx=10, pady=10)
    text_box.insert("1.0", content)
    text_box.configure(state="disabled")

root = Tk()
root.geometry("350x100")
root.title("Translate txt file")

nameVar = StringVar()

entryWidget = ctk.CTkEntry(root)
entryWidget.pack(side=TOP, padx=5, pady=5)

pathLabel = ctk.CTkLabel(root, text="Drag and drop file in the entry box")
pathLabel.pack(side=TOP)

entryWidget.drop_target_register(DND_ALL)
entryWidget.dnd_bind("<<Drop>>", get_text)

root.mainloop()
