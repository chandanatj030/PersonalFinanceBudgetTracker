from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import TransactionForm, BudgetForm, RegisterForm
from .models import Transaction, Budget,Category
from django.utils import timezone
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            login(request, user)

            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(
            request,
            'login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')

    total_income = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == 'income'
    )

    total_expenses = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == 'expense'
    )

    balance = total_income - total_expenses

    current_month = timezone.now().month
    current_year = timezone.now().year

    budget = Budget.objects.filter(
        user=request.user,
        month__year=current_year,
        month__month=current_month
    ).first()

    monthly_expenses = sum(
        transaction.amount
        for transaction in transactions
        if transaction.transaction_type == 'expense'
        and transaction.date.month == current_month
        and transaction.date.year == current_year
    )

    budget_amount = budget.amount if budget else 0

    if budget_amount > 0:
        budget_percentage = (monthly_expenses / budget_amount) * 100
    else:
        budget_percentage = 0

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'budget': budget,
        'budget_amount': budget_amount,
        'monthly_expenses': monthly_expenses,
        'budget_percentage': min(budget_percentage, 100),
    }

    return render(request, 'index.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(
    request,
    'Transaction added successfully!'
)
            return redirect('home')

    else:
        form = TransactionForm()

    return render(
        request,
        'add_transaction.html',
        {'form': form}
    )


@login_required
def add_income(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'income'
            transaction.save()

            return redirect('home')

    else:
        form = TransactionForm(
            initial={'transaction_type': 'income'}
        )

    return render(
        request,
        'add_transaction.html',
        {'form': form}
    )


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.transaction_type = 'expense'
            transaction.save()

            return redirect('home')

    else:
        form = TransactionForm(
            initial={'transaction_type': 'expense'}
        )

    return render(
        request,
        'add_transaction.html',
        {'form': form}
    )


@login_required
def set_budget(request):

    if request.method == 'POST':

        form = BudgetForm(request.POST)

        if form.is_valid():

            month = form.cleaned_data['month']
            amount = form.cleaned_data['amount']

            Budget.objects.update_or_create(
                user=request.user,
                month=month,
                defaults={
                    'amount': amount
                }
            )
            messages.success(
    request,
    'Budget saved successfully!'
)

            return redirect('home')

    else:

        form = BudgetForm()

    current_budget = Budget.objects.filter(
        user=request.user
    ).order_by('-month').first()

    budget_history = Budget.objects.filter(
        user=request.user
    ).order_by('-month')

    return render(
        request,
        'budget.html',
        {
            'form': form,
            'current_budget': current_budget,
            'budget_history': budget_history
        }
    )
def edit_budget(request, id):

    budget = get_object_or_404(
        Budget,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = BudgetForm(
            request.POST,
            instance=budget
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Budget updated successfully!'
            )

            return redirect('set_budget')

    else:

        form = BudgetForm(
            instance=budget
        )

    return render(
        request,
        'edit_budget.html',
        {'form': form}
    )
def delete_budget(request, id):

    budget = get_object_or_404(
        Budget,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        budget.delete()

        messages.success(
            request,
            'Budget deleted successfully!'
        )

    return redirect('set_budget')

@login_required
def transactions(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')

    transaction_type = request.GET.get('type')
    category = request.GET.get('category')
    date = request.GET.get('date')

    if transaction_type:
        transactions = transactions.filter(
            transaction_type=transaction_type
        )

    if category:
        transactions = transactions.filter(
            category_id=category
        )

    if date:
        transactions = transactions.filter(
            date=date
        )

    categories = Category.objects.all()

    return render(
        request,
        'transactions.html',
        {
            'transactions': transactions,
            'categories': categories,
            'selected_type': transaction_type,
            'selected_category': category,
            'selected_date': date
        }
    )


def edit_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Transaction updated successfully!'
            )

            return redirect('transactions')

    else:

        form = TransactionForm(
            instance=transaction
        )

    return render(
        request,
        'edit_transaction.html',
        {'form': form}
    )

def delete_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        transaction.delete()

        messages.success(
            request,
            'Transaction deleted successfully!'
        )

    return redirect('transactions')