import tkinter as tk
from tkinter import messagebox
import os
import sqlite3

def init_db():
    if not os.path.exists("data"):
        os.mkdir("data")
    
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT UNIQUE NOT NULL,
                   password TEXT NOT NULL
                   )
                   
                   """)
    conn.commit()
    conn.close()
    
def register():
    name = entry_username.get()
    passw = entry_password.get()
    
    if not name or not passw:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun. ")
        return
    
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                       INSERT INTO users (username,password) VALUES(?,?)
                       
                       """,(name,passw))
        conn.commit()
        messagebox.showinfo("Başarılı", "Kayıt başarılı! Giriş yapabilirsiniz.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut.")
    conn.close()
    
def login():
    name = entry_username.get()
    passw = entry_password.get()
    
    if not name or not passw:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun. ")
        return

    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = ? AND passw = ?",(name,passw))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Giriş Başarılı", f"Hoş geldiniz, {name}!")
        root.destroy()
        import dashboard
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