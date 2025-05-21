import tkinter as tk
from tkinter import messagebox
import os
import sqlite3

from db import init_db, login_user, register_user

    
def register():
    name = entry_username.get()
    passw = entry_password.get()

    if not name or not passw:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
        return

    if register_user(name, passw):
        messagebox.showinfo("Başarılı", "Kayıt başarılı! Giriş yapabilirsiniz.")
    else:
        messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut.")

    
    
    
   
    
def login():
    name = entry_username.get()
    passw = entry_password.get()

    if not name or not passw:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun.")
        return

    if login_user(name, passw):
        messagebox.showinfo("Giriş Başarılı", f"Hoş geldiniz, {name}!")
        root.destroy()
        import dashboard
        dashboard.run_dashboard(name)
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı.")
  
    
    

root = tk.Tk()
root.title("Akıllı Bütçe - Giriş")
root.geometry("300x200")
root.resizable(False, False)

tk.Label(root, text="Kullanıcı Adı:").pack(pady=(20, 0))
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Şifre:").pack(pady=(10, 0))
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Giriş Yap", command=login).pack(pady=(15, 5))
tk.Button(root, text="Kayıt Ol", command=register).pack()

init_db()
root.mainloop()