import os
import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'finance_tracker.settings'
)

django.setup()

from fastapi import FastAPI, Request, HTTPException
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User


app = FastAPI(
    title="Personal Finance Budget Tracker API"
)


def get_logged_in_user(request: Request):

    session_id = request.cookies.get('sessionid')

    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Login required."
        )

    session = SessionStore(session_key=session_id)

    if not session.exists(session_id):
        raise HTTPException(
            status_code=401,
            detail="Invalid session."
        )

    user_id = session.get('_auth_user_id')

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Login required."
        )

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=401,
            detail="User not found."
        )


@app.get("/")
def home():

    return {
        "message": "Personal Finance Budget Tracker API is running!"
    }


@app.get("/api/transactions/")
def get_transactions(request: Request):

    from tracker.models import Transaction

    user = get_logged_in_user(request)

    transactions = Transaction.objects.filter(
        user=user
    )

    return [
        {
            "id": transaction.id,
            "type": transaction.transaction_type,
            "amount": float(transaction.amount),
            "description": transaction.description,
            "date": str(transaction.date)
        }
        for transaction in transactions
    ]


@app.get("/api/budget/")
def get_budget(request: Request):

    from tracker.models import Budget

    user = get_logged_in_user(request)

    budgets = Budget.objects.filter(
        user=user
    )

    return [
        {
            "id": budget.id,
            "month": str(budget.month),
            "amount": float(budget.amount)
        }
        for budget in budgets
    ]


@app.get("/api/summary/")
def get_summary(request: Request):

    from tracker.models import Transaction, Budget
    from django.db.models import Sum

    user = get_logged_in_user(request)

    total_income = Transaction.objects.filter(
        user=user,
        transaction_type='income'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_expenses = Transaction.objects.filter(
        user=user,
        transaction_type='expense'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    total_budget = Budget.objects.filter(
        user=user
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    balance = total_income - total_expenses

    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "balance": float(balance),
        "total_budget": float(total_budget)
    }