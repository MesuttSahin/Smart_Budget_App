from datetime import datetime
import db

def get_user_statistics(username):
    total_income = db.get_total_income(username)
    total_expense = db.get_total_expense(username)
    top_category, top_category_amount = db.get_most_spent_category(username)
    avg_monthly_expense = db.get_avg_monthly_expense(username)

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_budget": total_income - total_expense,
        "top_category": top_category,
        "top_category_amount": top_category_amount,
        "avg_monthly_expense": avg_monthly_expense
    }


def get_daily_summary(username):
    today = datetime.today().strftime("%d / %m / %Y")
    return db.get_total_by_date(username, today)

def get_monthly_summary(username):
    now = datetime.now()
    return db.get_total_by_month(username, now.year, now.month)