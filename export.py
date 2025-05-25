import sqlite3
import csv
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox

DB_PATH = "data/butce.db"

def export_to_csv(username):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT date, username ,types, amount
            FROM transactions
            WHERE username = ?
            ORDER BY date
        """, (username,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Bilgi", "Hiç kayıt bulunamadı.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV dosyası", "*.csv")],
            initialfile=f"export_{username}_{datetime.today().strftime('%d-%m-%Y')}.csv"
        )

        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Tarih", "Başlık", "Tür", "Tutar"])  
                writer.writerows(rows)
            messagebox.showinfo("Başarılı", f"Veriler dışa aktarıldı:\n{filename}")
        else:
            messagebox.showinfo("İptal", "Dışa aktarma iptal edildi.")

    except Exception as e:
        messagebox.showerror("Hata", f"CSV dışa aktarımında hata oluştu:\n{e}")
