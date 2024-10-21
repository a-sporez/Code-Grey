import tkinter as tk
from tkinter import filedialog, messagebox
import markdown
import os

def convert_markdown_file(input_file, output_file):
    """
    Convert a Markdown file to an HTML file.
    
    Args:
        input_file (str): Path to the input Markdown file.
        output_file (str): Path to the output HTML file.
    """
    with open(input_file, 'r', encoding='utf-8') as md_file:
        markdown_text = md_file.read()

    html = markdown.markdown(markdown_text)

    with open(output_file, 'w', encoding='utf-8') as html_file:
        html_file.write(html)

def browse_input_file():
    input_file_path = filedialog.askopenfilename(
        title="Select Markdown File",
        filetypes=(("Markdown files", "*.md"), ("All files", "*.*"))
    )
    input_file_entry.delete(0, tk.END)  # Clear the entry first
    input_file_entry.insert(0, input_file_path)

def browse_output_file():
    output_file_path = filedialog.asksaveasfilename(
        title="Save as HTML File",
        defaultextension=".html",
        filetypes=(("HTML files", "*.html"), ("All files", "*.*"))
    )
    output_file_entry.delete(0, tk.END)  # Clear the entry first
    output_file_entry.insert(0, output_file_path)

def convert_file():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    
    if not input_file or not output_file:
        messagebox.showwarning("Warning", "Both input and output file paths must be provided!")
        return
    
    try:
        convert_markdown_file(input_file, output_file)
        messagebox.showinfo("Success", f"Converted {os.path.basename(input_file)} to {os.path.basename(output_file)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Set up the Tkinter window
root = tk.Tk()
root.title("Markdown to HTML Converter")

# Create and place widgets
tk.Label(root, text="Select Markdown File:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)
browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Save HTML File As:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)
browse_output_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_output_button.grid(row=1, column=2, padx=10, pady=5)

convert_button = tk.Button(root, text="Convert", command=convert_file)
convert_button.grid(row=2, column=1, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()