from setuptools import setup, find_packages
import tkinter as tk
from tkinter import messagebox

def show_popup():
    messagebox.showinfo("ceshigogo", "ceshigogo setup1111111111111111111111")
 

root = tk.Tk()
print("123123123123laksdkasgdka")
root.withdraw()  
show_popup()
root.mainloop()

print("ceshigogo setup1111111111111111111111")

setup(
    packages=find_packages(),
)
