from datetime import datetime, date

import pymysql
from contextlib import contextmanager, closing
from logging_setup import setup_logger

logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="vishal",
        database="expense_manager",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor    #enable dictionary output , fetch data in dict format
    )
   # return connection.cursor(),connection
    print("Connection successful")
    cursor = connection.cursor()
    yield cursor
    if commit:
        connection.commit()

    cursor.close()
    connection.close()
    print("Connection Closed")
'''def fetch_all_records():
    with get_db_cursor() as cursor:

        cursor.execute("SELECT* FROM expenses")
        expenses=cursor.fetchall()
        for expense in expenses: 
            print(expense)'''

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")

    if isinstance(expense_date, str):
        expense_date=datetime.strptime(expense_date,"%Y-%m-%d").date()
    with get_db_cursor() as cursor:
        print("Connected to DB...")
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses=cursor.fetchall()
        # for expense in expenses:
        #     print(expense)
        print(f"Fetched {len(expenses)} expenses")
        return expenses


def insert_expense(expense_date, amount, category,notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category,notes) VALUES (%s,%s,%s,%s)",
            (expense_date,amount,category,notes)
                       )
def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date=%s",(expense_date,))

def fetch_expenses_summary(start_date,end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date}, end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
            FROM expenses WHERE expense_date 
            BETWEEN %s and %s
            GROUP BY category;''',
            (start_date,end_date)
        )
        data=cursor.fetchall()
        return data
if __name__=="__main__":
    # expenses=fetch_expenses_for_date("2024-08-01")
    # print(expenses)
    #insert_expense("2024-08-25",40,"food","Eat somosa")
    #delete_expenses_for_date("2024-08-25")
    summary=fetch_expenses_summary("2024-08-01","2024-08-05")
    for record in summary:
        print(record)