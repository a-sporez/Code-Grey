import tkinter as tk
from tkinter import filedialog

def save_file():
    # Open a file dialog to select the save location and file name
    file_path = filedialog.asksaveasfilename(defaultextension=".gs",
                                             filetypes=[("GreyScript Files", "*.gs"), ("All Files", "*.*")])
    if file_path:
        # Write the content of the editor to the selected file
        with open(file_path, "w") as file:
            # "1.0" means from the first line, first character
            file.write(editor.get("1.0", tk.END).strip())

# function to load a .gs file into the editor
def load_file():
    # Open a file dialog to select the file to load.
    file_path = filedialog.askopenfilename(filetypes=[("GreyScipt File", "*.gs"), ("All Files", "*.*")])
    if file_path:
        # Clear the current content of the editor and load the selected file
        with open(file_path, "r") as file:
            editor.delete("1.0", tk.END) # Clear existing text
            editor.insert("1.0", file.read()) # Insert the file content

# Function to apply syntax highlighting
def apply_highlighting(event=None):
    editor.tag_remove("keyword", "1.0", tk.END) # Remove existing tag
    editor.tag_remove("function", "1.0", tk.END)
    editor.tag_remove("string", "1.0", tk.END)

    keywords = ["var", "function", "if", "else", "for", "while", "return"]
    functions = ["Socket", "File", "Process"]

    for keyword in keywords:
        start = "1.0"
        while True:
            start = editor.search(f"\\b{keyword}\\b", start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(keyword)}c"
            editor.tag_add("keyword", start, end)
            start = end