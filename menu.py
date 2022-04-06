from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

# root window
root = tk.Tk()
root.geometry("600x200")
root.title('Démineur')
root.resizable(0, 0)

# configure the grid
root.columnconfigure(0, weight=2)
root.columnconfigure(1, weight=2)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
root.columnconfigure(6, weight=1)
root.columnconfigure(7, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)

def msgCallBack():
    messagebox.showinfo("App", "La partie va commencer !")

login_button = ttk.Label(root)
login_button.grid(column= 0, row=1)

login_button = ttk.Button(root, text="Simple")
login_button.grid(column= 1, row=1)

login_button = ttk.Button(root, text="Medium")
login_button.grid(column= 2, row=1)

login_button = ttk.Button(root, text="Difficile")
login_button.grid(column= 3, row=1)

login_button = ttk.Button(root, text="Personaliser")
login_button.grid(column= 4, row=1)

login_button = ttk.Label(root)
login_button.grid(column= 5, row=1)

login_button = ttk.Button(root, text="Start", command = msgCallBack)
login_button.grid(column= 2, row=2, columnspan=2)

root.mainloop()