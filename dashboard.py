import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import os

def init_transaction_db():
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS transactions(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            category TEXT NOT NULL,
                            amount REAL NOT NULL,
                            date TEXT NOT NULL,
                            types TEXT CHECK(types IN ('Gelir', 'Harcama')) NOT NULL)
                                                            

                   
                   """)
    conn.commit()
    conn.close()
    
def add_transactions(username,category,amount,date,transac_type):
    if not category or not amount or not date or not transac_type:
        messagebox.showwarning("Eksik Bilgi","Lütfen tüm alanları doldurunuz")
        return
    
    try:
        amount = float(amount)
        
    except ValueError:
        messagebox.showerror("Hatalı Giriş", "Miktar sayısal bir değer olmalıdır.")
        return
    
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO transactions (username, category, amount, date, types)
                   VALUES(?, ?, ?, ?, ?)
                   """,(username,category,amount,date,transac_type))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi.")
    
root = tk.Tk()
root.title("Akıllı Bütçe - Ana Panel")
root.geometry("900x600")
root.configure(padx=10,pady=10)

categories = ["Yiyecek","Ulaşım","Kira","Maaş","Eğlence","Fatura","Diğer"]

frame_left = tk.LabelFrame(root,text="Harcama / Gelir Ekle",padx=10,pady=10)
frame_left.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)

tk.Label(frame_left,text="Kategori:").grid(row=0,column=0,sticky="w")
combo_category = ttk.Combobox(frame_left,values=categories)
combo_category.grid(row=0,column=1)

tk.Label(frame_left,text="Miktar (TL): ").grid(row=1,column=0,sticky="w")
entry_amount = tk.Entry(frame_left)
entry_amount.grid(row=1,column=1)

tk.Label(frame_left,text="Tarih (GG/AA/YYYY):").grid(row=2,column=0,sticky="w")
entry_date = tk.Entry(frame_left)
entry_date.insert(0,datetime.today().strftime("%d / %m /%Y"))
entry_date.grid(row=2,column=1)

tk.Label(frame_left,text="Tür:").grid(row=3,column=0,sticky="w")
type_var = tk.StringVar()
type_var.set("Harcama")
tk.Radiobutton(frame_left, text="Harcama", variable=type_var, value="Harcama").grid(row=3, column=1, sticky="w")
tk.Radiobutton(frame_left, text="Gelir", variable=type_var, value="Gelir").grid(row=3, column=1, sticky="e")

tk.Button(frame_left, text="Ekle", width=20, command=lambda: add_transactions("testuser",combo_category.get(),entry_amount.get(),entry_date.get(),type_var.get())).grid(row=4, column=0, columnspan=2, pady=10)

frame_right = tk.LabelFrame(root, text="Özet Bilgiler", padx=10, pady=10)
frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

label_daily_total = tk.Label(frame_right, text="Günlük Toplam: ₺0")
label_daily_total.pack()

label_monthly_total = tk.Label(frame_right, text="Aylık Toplam: ₺0")
label_monthly_total.pack()

frame_graph = tk.LabelFrame(root, text="Grafikler", padx=10, pady=10)
frame_graph.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
tk.Label(frame_graph, text="Grafikler burada gösterilecek (matplotlib)").pack()

frame_bottom = tk.LabelFrame(root, text="Filtreleme ve İşlemler", padx=10, pady=10)
frame_bottom.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

tk.Label(frame_bottom, text="Tarih Aralığı:").grid(row=0, column=0)
tk.Entry(frame_bottom, width=12).grid(row=0, column=1)
tk.Label(frame_bottom, text="-").grid(row=0, column=2)
tk.Entry(frame_bottom, width=12).grid(row=0, column=3)

tk.Label(frame_bottom, text="Kategori:").grid(row=0, column=4)
ttk.Combobox(frame_bottom, values=["Tümü"] + categories).grid(row=0, column=5)

tk.Button(frame_bottom, text="Filtrele").grid(row=0, column=6, padx=10)
tk.Button(frame_bottom, text="Döviz Güncelle").grid(row=0, column=7, padx=5)
tk.Button(frame_bottom, text="Veri Dışa Aktar").grid(row=0, column=8, padx=5)
tk.Button(frame_bottom, text="Çıkış", command=root.quit).grid(row=0, column=9, padx=10)

init_transaction_db()
root.mainloop()