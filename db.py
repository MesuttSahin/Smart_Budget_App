import os
import sqlite3
from tkinter import messagebox
from datetime import datetime

DB_PATH = "data/butce.db"

def init_transaction_db():
    if not os.path.exists("data"):
        os.mkdir("data")
    conn = sqlite3.connect(DB_PATH)
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

def add_transaction(username, category, amount, date, transac_type):
    if not category or not amount or not date or not transac_type:
        messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurunuz")
        return False

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Hatalı Giriş", "Miktar sayısal bir değer olmalıdır.")
        return False

    try:
        datetime.strptime(date.strip(), "%d / %m / %Y")
    except ValueError:
        messagebox.showerror("Hatalı Giriş", "Tarih formatı GG / AA / YYYY olmalıdır.")
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO transactions (username, category, amount, date, types)
                   VALUES (?, ?, ?, ?, ?)
                   """, (username, category, amount, date, transac_type))
    conn.commit()
    conn.close()
    return True


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
    
def register_user(username,password):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
                       INSERT INTO users (username,password) VALUES(?,?)
                       
                       """,(username,password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
        
def login_user(username,password):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT * FROM users WHERE username = ? AND password = ? 
                   """,(username,password))
    user = cursor.fetchone()
    conn.close()
    return user




def get_filtered_transactions(username, start_date=None, end_date=None, category=None, transac_type=None):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()

    query = "SELECT * FROM transactions WHERE username = ?"
    params = [username]

    if category:
        query += " AND category = ?"
        params.append(category)
    if transac_type:
        query += " AND types = ?"
        params.append(transac_type)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


def delete_transaction(trans_id):
    conn = sqlite3.connect("data/butce.db")
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
    conn.commit()
    conn.close()

def update_transaction(trans_id, category, amount, date, transac_type):
    conn = sqlite3.connect("data/butce.db")
    c = conn.cursor()
    c.execute("""
        UPDATE transactions SET 
            category=?, 
            amount=?, 
            date=?, 
            types=?
        WHERE id=?
    """, (category, amount, date, transac_type, trans_id))
    conn.commit()
    conn.close()

def get_transactions_by_category(username):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE username = ? AND types = 'Harcama'
        GROUP BY category
    """, (username,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_total_income(username):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT SUM(amount) FROM transactions
                   WHERE username=? AND types="Gelir"
                   
                   """,(username,))
    result = cursor.fetchone()[0] or 0
    conn.close()
    return result

def get_total_expense(username):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE username=? AND types='Harcama'
    """, (username,))
    result = cursor.fetchone()[0] or 0
    conn.close()
    return result

def get_most_spent_category(username):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT category, SUM(amount) as total FROM transactions 
        WHERE username=? AND types='Harcama' 
        GROUP BY category ORDER BY total DESC LIMIT 1
    """, (username,))
    row = cursor.fetchone()
    conn.close()
    return row if row else (None, 0)

def get_avg_monthly_expense(username):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%Y-%m', date) as month, SUM(amount) 
        FROM transactions 
        WHERE username=? AND types='Harcama'
        GROUP BY month
    """, (username,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return 0
    return sum(row[1] for row in rows) / len(rows)

def get_total_by_date(username, date_str):
    conn = sqlite3.connect("data/butce.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT types, SUM(amount)
        FROM transactions
        WHERE username = ? AND date = ?
        GROUP BY types
    """, (username, date_str))
    rows = cursor.fetchall()
    conn.close()

    summary = {"income": 0.0, "expense": 0.0}
    for t_type, total in rows:
        if t_type == "Gelir":
            summary["income"] = total
        elif t_type == "Harcama":
            summary["expense"] = total
    return summary


def get_total_by_month(username, year, month):
    month_str = f"{month:02d}"
    year_str = str(year)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT types, SUM(amount)
        FROM transactions
        WHERE username = ?
          AND substr(date, 11, 4) = ?
          AND substr(date, 6, 2) = ?
        GROUP BY types
    """, (username, year_str, month_str))
    rows = cursor.fetchall()
    conn.close()

    summary = {"income": 0.0, "expense": 0.0}
    for t_type, total in rows:
        if t_type == "Gelir":
            summary["income"] = total
        elif t_type == "Harcama":
            summary["expense"] = total
    return summary


    


    