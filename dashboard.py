import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import db
from db import get_filtered_transactions

current_user = None  # Global kullanıcı adı

def run_dashboard(username):
    global current_user
    current_user = username

    root = tk.Tk()
    root.title(f"Akıllı Bütçe - Ana Panel - Hoşgeldiniz {username}")
    root.geometry("900x600")
    root.configure(padx=10, pady=10)

    categories = ["Yiyecek", "Ulaşım", "Kira", "Maaş", "Eğlence", "Fatura", "Diğer"]

    def on_filter():
        category = combo_filter_category.get()
        transac_type = combo_filter_type.get()

        if not category or category == "Tümü":
            category = None
        if not transac_type or transac_type == "Tümü":
            transac_type = None

        try:
            results = get_filtered_transactions(current_user, None, None, category, transac_type)

            for item in tree.get_children():
                tree.delete(item)

            for row in results:
                tree.insert("", "end", values=row)

            messagebox.showinfo("Filtreleme Başarılı", f"{len(results)} kayıt listelendi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Filtreleme hatası:\n{e}")

    def on_add_transaction():
        category = combo_category.get()
        amount = entry_amount.get()
        date = entry_date.get()
        transac_type = type_var.get()

        success = db.add_transaction(current_user, category, amount, date, transac_type)
        if success:
            messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi.")
            combo_category.set('')
            entry_amount.delete(0, tk.END)
            entry_date.delete(0, tk.END)
            entry_date.insert(0, datetime.today().strftime("%d / %m / %Y"))
            type_var.set("Harcama")

    # Sol panel - Harcama/Gelir Ekle
    frame_left = tk.LabelFrame(root, text="Harcama / Gelir Ekle", padx=10, pady=10)
    frame_left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    tk.Label(frame_left, text="Kategori:").grid(row=0, column=0, sticky="w")
    combo_category = ttk.Combobox(frame_left, values=categories)
    combo_category.grid(row=0, column=1)

    tk.Label(frame_left, text="Miktar (TL): ").grid(row=1, column=0, sticky="w")
    entry_amount = tk.Entry(frame_left)
    entry_amount.grid(row=1, column=1)

    tk.Label(frame_left, text="Tarih (GG / AA / YYYY):").grid(row=2, column=0, sticky="w")
    entry_date = tk.Entry(frame_left)
    entry_date.insert(0, datetime.today().strftime("%d / %m / %Y"))
    entry_date.grid(row=2, column=1)

    tk.Label(frame_left, text="Tür:").grid(row=3, column=0, sticky="w")
    type_var = tk.StringVar(value="Harcama")
    tk.Radiobutton(frame_left, text="Harcama", variable=type_var, value="Harcama").grid(row=3, column=1, sticky="w")
    tk.Radiobutton(frame_left, text="Gelir", variable=type_var, value="Gelir").grid(row=3, column=1, sticky="e")

    tk.Button(frame_left, text="Ekle", width=20, command=on_add_transaction).grid(row=4, column=0, columnspan=2, pady=10)

    # Sağ panel - Özet Bilgiler
    frame_right = tk.LabelFrame(root, text="Özet Bilgiler", padx=10, pady=10)
    frame_right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    label_daily_total = tk.Label(frame_right, text="Günlük Toplam: ₺0")
    label_daily_total.pack()

    label_monthly_total = tk.Label(frame_right, text="Aylık Toplam: ₺0")
    label_monthly_total.pack()

    # Grafik alanı
    frame_graph = tk.LabelFrame(root, text="Grafikler", padx=10, pady=10)
    frame_graph.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    tk.Label(frame_graph, text="Grafikler burada gösterilecek (matplotlib)").pack()

    # Alt panel - filtreleme alanı
    frame_bottom = tk.LabelFrame(root, text="Filtreleme ve İşlemler", padx=10, pady=10)
    frame_bottom.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    tk.Label(frame_bottom, text="Tür:").grid(row=0, column=0)
    combo_filter_type = ttk.Combobox(frame_bottom, values=["Tümü", "Harcama", "Gelir"])
    combo_filter_type.set("Tümü")
    combo_filter_type.grid(row=0, column=1)

    tk.Label(frame_bottom, text="Kategori:").grid(row=0, column=2)
    combo_filter_category = ttk.Combobox(frame_bottom, values=["Tümü"] + categories)
    combo_filter_category.set("Tümü")
    combo_filter_category.grid(row=0, column=3)

    tk.Button(frame_bottom, text="Filtrele", command=on_filter).grid(row=0, column=4, padx=10)
    tk.Button(frame_bottom, text="Döviz Güncelle").grid(row=0, column=5, padx=5)
    tk.Button(frame_bottom, text="Veri Dışa Aktar").grid(row=0, column=6, padx=5)
    tk.Button(frame_bottom, text="Çıkış", command=root.quit).grid(row=0, column=7, padx=10)

    # Treeview
    columns = ("id", "username", "category", "amount", "date", "type")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    # Başlıkları ayarla
    tree.heading("id", text="ID")
    tree.heading("username", text="Kullanıcı")
    tree.heading("category", text="Kategori")
    tree.heading("amount", text="Miktar")
    tree.heading("date", text="Tarih")
    tree.heading("type", text="Tür")

    # Sütun genişlikleri
    tree.column("id", width=30, anchor="center")
    tree.column("username", width=100, anchor="center")
    tree.column("category", width=100, anchor="center")
    tree.column("amount", width=80, anchor="center")
    tree.column("date", width=100, anchor="center")
    tree.column("type", width=80, anchor="center")

    tree.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    # Grid ayarları
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Veritabanını başlat
    db.init_transaction_db()

    root.mainloop()