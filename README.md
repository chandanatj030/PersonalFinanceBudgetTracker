# Personal Finance & Budget Tracker

A Python-based personal finance and budget tracking web application built to help users manage income, expenses, budgets, and financial summaries securely.

## Features

- User registration and login
- Secure user-specific data
- Add income and expenses
- Categorize transactions
- Edit and delete transactions
- Filter transactions by type, category, and date
- Set and manage monthly budgets
- Edit and delete budgets
- Dashboard with:
  - Total income
  - Total expenses
  - Remaining balance
  - Monthly budget progress
  - Financial overview charts
  - Recent transactions
- FastAPI endpoints for financial data
- MySQL database integration
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
- MySQL

### Tools
- Git
- GitHub
- MySQL Workbench
- VS Code

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
## How to Run Locally

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Configure the required environment variables.
5. Apply Django migrations.
6. Start the Django development server.

Example:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver