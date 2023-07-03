import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import re

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as file:
            code_text.delete("1.0", tk.END)
            code_text.insert(tk.END, file.read())
            highlight_syntax()

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(code_text.get("1.0", tk.END))

def run_code():
    code = code_text.get("1.0", tk.END)
    try:
        subprocess.run(["python", "-c", code], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"An error occurred: {e.stderr}")

def auto_indent(event):
    code_text.tag_remove("sel", "1.0", tk.END)
    current_line = code_text.index(tk.INSERT).split('.')[0]
    previous_line = str(int(current_line) - 1)
    previous_line_indent = code_text.get(previous_line + ".0", previous_line + ".end").strip()
    if previous_line_indent.endswith(":"):
        indent = " " * (len(previous_line_indent) - len(previous_line_indent.lstrip()) + 4)
        code_text.insert(tk.INSERT, indent)

def highlight_syntax(event=None):
    code_text.tag_remove("syntax", "1.0", tk.END)

    keywords = ["def", "class", "if", "else", "elif", "for", "while", "try", "except", "finally", "with", "as",
                "import", "from", "global", "nonlocal", "return", "yield", "assert", "lambda", "pass", "break",
                "continue", "in", "not", "is", "and", "or", "True", "False", "None"]

    string_pattern = r"\".*?\"|\'.*?\'"
    comment_pattern = r"#.*?$"

    code = code_text.get("1.0", tk.END)
    tags = []

    for keyword in keywords:
        for match in re.finditer(r"\b{}\b".format(re.escape(keyword)), code):
            start = match.start()
            end = match.end()
            code_text.tag_add("syntax", f"1.0+{start}c", f"1.0+{end}c")

    for pattern, tag in [(string_pattern, "string"), (comment_pattern, "comment")]:
        for match in re.finditer(pattern, code, re.MULTILINE):
            start = match.start()
            end = match.end()
            code_text.tag_add(tag, f"1.0+{start}c", f"1.0+{end}c")

    code_text.tag_config("syntax", foreground="blue")
    code_text.tag_config("string", foreground="green")
    code_text.tag_config("comment", foreground="red")

root = tk.Tk()
root.title("Python Code Editor")

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

run_menu = tk.Menu(menu_bar, tearoff=False)
run_menu.add_command(label="Run", command=run_code)
menu_bar.add_cascade(label="Run", menu=run_menu)

root.config(menu=menu_bar)

editor_frame = tk.Frame(root)
editor_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(editor_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

code_text = tk.Text(editor_frame, wrap=tk.NONE, yscrollcommand=scrollbar.set)
code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=code_text.yview)

code_text.bind("<Tab>", auto_indent)
code_text.bind("<KeyRelease>", highlight_syntax)
code_text.tag_configure("syntax", foreground="blue")
code_text.tag_configure("string", foreground="green")
code_text.tag_configure("comment", foreground="red")

root.mainloop()
