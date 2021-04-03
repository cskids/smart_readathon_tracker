import tkinter as tk

from datetime import date
from pathlib import Path

# http://www.science.smith.edu/dftwiki/images/3/3d/TkInterColorCharts.png
BG_COLOR = 'gold'
BUTTON_COLOR = 'SlateGray4'

FONT = 'arial 12 bold'
DATA_FILE = 'data.txt'

def set_listbox():
    listbox.delete(0, tk.END)
    for book_title, _, _, _ in books:
        listbox.insert(tk.END, book_title)

def write_to_file():
    with open(DATA_FILE, 'w') as f:
        for book_title, book_author, book_isbn, complete_date in books:
            f.write(f"{book_title}|{book_author}|{book_isbn}|{complete_date}\n")

def save():
    if not title.get() or not author.get():
        return
    if listbox.curselection():
        edit_book()
    else:
        add_book()
    set_listbox()
    reset()
    write_to_file()

def reset():
    title.set('')
    author.set('')
    isbn.set('')
    title_entry.focus_set()

def add_book():
    today = date.today()
    books.append([title.get(), author.get(), isbn.get(), today.strftime("%Y-%m-%d")])

def edit_book():
    selected = listbox.curselection()[0]
    read_date = books[selected][3]
    books[selected] = [title.get(), author.get(), isbn.get(), read_date]

def delete_book():
    selection = listbox.curselection()
    if not selection:
        return
    selected = selection[0]
    del books[selected]
    set_listbox()
    reset()
    write_to_file()

def listbox_callback(event):
    selection = listbox.curselection()
    if selection:
        book_title, book_author, book_isbn, _ = books[selection[0]]
        title.set(book_title)
        author.set(book_author)
        isbn.set(book_isbn)

window = tk.Tk()
window.geometry('400x400')
window.config(bg=BG_COLOR)
window.resizable(0, 0)
window.title("Smart Readathon Tracker")

frame = tk.Frame(window)
frame.pack(side=tk.BOTTOM)

title = tk.StringVar()
author = tk.StringVar()
isbn = tk.StringVar()

# Title
tk.Label(window, text='Title', font=FONT, bg=BG_COLOR).place(x=10, y=20)
title_entry = tk.Entry(window, textvariable=title, width=40)
title_entry.place(x=100, y=20)

# Author
tk.Label(window, text='Author', font=FONT, bg=BG_COLOR).place(x=10, y=45)
author_entry = tk.Entry(window, textvariable=author, width=40)
author_entry.place(x=100, y=45)

# ISBN
tk.Label(window, text='ISBN', font=FONT, bg=BG_COLOR).place(x=10, y=70)
isbn_entry = tk.Entry(window, textvariable=isbn, width=40)
isbn_entry.place(x=100, y=70)

# Listbox and scroll bar
scroll = tk.Scrollbar(frame, orient=tk.VERTICAL)
listbox = tk.Listbox(frame, yscrollcommand=scroll.set, height=15, width=100, exportselection=False, selectmode=tk.SINGLE)
scroll.config(command=listbox.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

books = []

if Path(DATA_FILE).exists():
    with open(DATA_FILE) as f:
        for line in f:
            books.append(line.strip().split("|"))

listbox.bind("<<ListboxSelect>>", listbox_callback)

tk.Button(window, text='SAVE', font=FONT, bg=BUTTON_COLOR, command=save).place(x=10, y=110)
tk.Button(window, text='DELETE', font=FONT, bg=BUTTON_COLOR, command=delete_book).place(x=100, y=110)

set_listbox()
window.mainloop()
