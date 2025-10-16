from tkinter import StringVar, TOP
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
from pathlib import Path


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
        show_file_content(file_content,file_name)
    except Exception as e:
        pathLabel.configure(text=f"Error: {e}")

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
