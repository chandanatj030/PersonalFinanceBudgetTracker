# Personal Finance & Budget Tracker

A Python-based full-stack web application that helps users manage income, expenses, monthly budgets, and financial summaries securely.

## Features

- User registration and login
- User-specific financial data
- Add income and expenses
- Categorize transactions
- Edit and delete transactions
- Filter transactions by type, category, and date
- Create, edit, and delete monthly budgets
- Dashboard with income, expenses, balance, and budget information
- Financial overview charts
- FastAPI endpoints for financial data
- JWT-based API authentication
- Form validation
- Automated Django tests
- Environment-based configuration for sensitive settings

## Technologies Used

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

### Backend

- Python
- Django
- FastAPI

### Database

- MySQL for local development
- PostgreSQL for production deployment

### Tools

- Git
- GitHub
- MySQL Workbench
- VS Code
- Render

## Project Structure

```text
PersonalFinanceBudgetTracker/
│
├── finance_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tracker/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── transactions.html
│   ├── add_transaction.html
│   ├── edit_transaction.html
│   ├── budget.html
│   └── edit_budget.html
│
├── fastapi_app.py
├── manage.py
├── .gitignore
└── README.md