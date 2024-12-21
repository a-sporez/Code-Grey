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
            editor.delete("1.0", tk.END)            # Clear existing text
            editor.insert("1.0", file.read())       # Insert the file content

# Function to apply syntax highlighting
def apply_highlighting(event=None):
    editor.tag_remove("keyword", "1.0", tk.END)     # Remove existing tag
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

    for func in functions:
        start = "1.0"
        while True:
            start = editor.search(f"\\b{func}\\b", start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(func)}c"
            editor.tag_add("function", start, end)
            start = end

    start = "1.0"
    while True:
        start = editor.search(r'".*?"', start, stopindex=tk.END, regexp=True)
        if not start:
            break
        end = editor.index(f"{start} lineend")
        editor.tag_add("string", start, end)
        start = end

# Root window
# The main application window for the editor

root = tk.Tk()
root.title("GreyScript Editor") # Window title
root.geometry("800x600")        # Default size of the window
root.configure(bg="black")

# Editor Area
# This is the text widget where users write and edit their code
editor = tk.Text(root,
                bg="black",               # Background
                fg="white",               # default text color
                insertbackground="white", # Cursor color
                font=("Courier", 12),     # Monospaced font
                wrap="none",              # Disable text wrapping for readability
                tabs=("0.5c",))           # 0.5cm tab width for GreyScript indentation
editor.pack(fill=tk.BOTH, expand=1)

# define syntax highlights tags
editor.tag_configure("keyword", foreground="cyan")
editor.tag_configure("function", foreground="lightgreen")
editor.tag_configure("string", foreground="yellow")

editor.bind("<KeyRelease>", apply_highlighting)

# Adding a basic menu for file operations
menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)                    # Create submenu for File operations
file_menu.add_command(label="Save", command=save_file)  # Add Save option
file_menu.add_command(label="Open", command=load_file)  # Add "Open" option
menu.add_cascade(label="File", menu=file_menu)          # Add the File menu to the menu bar
root.config(menu=menu)                                  # Attach menu to root window

# Tkinter main event loop
root.mainloop()