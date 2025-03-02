from http.client import HTTPException

from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

app=FastAPI()


class Expense(BaseModel):  # Data Validation(Pydantic)
    amount:float
    category:str
    notes:str

class DateRange(BaseModel):
    start_date:date
    end_date:date


@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

# api to fetch data by given date
@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):  # known as data validation or typehint in python
    print(f"Received GET request for {expense_date}")
    expenses = db_helper.fetch_expenses_for_date(expense_date)

    # Debug print
    print(f"Fetched expenses: {expenses}")

    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve")

    return expenses

# api to insert new data
@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date:date,expenses:List[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date,expense.amount,expense.category,expense.notes)
    return {"message": "Expenses updated successfully."}

# api to get data for date range for analytics purpose
@app.post("/analytics")
def get_analytics(date_range:DateRange):
    data=db_helper.fetch_expenses_summary(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve")

    total =sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage=(row['total']/total)*100 if total!=0 else 0
        breakdown[row['category']]={
            "total":row['total'],
            "percentage":percentage
        }
    return breakdown