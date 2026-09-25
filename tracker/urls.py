from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('login/', views.login_user, name='login'),

    path('logout/', views.logout_user, name='logout'),

    path('add-transaction/', views.add_transaction, name='add_transaction'),

    path('add-income/', views.add_income, name='add_income'),

    path('add-expense/', views.add_expense, name='add_expense'),

    path('set-budget/', views.set_budget, name='set_budget'),
    path(
    'budget/edit/<int:id>/',
    views.edit_budget,
    name='edit_budget'
),
path(
    'budget/delete/<int:id>/',
    views.delete_budget,
    name='delete_budget'
),

    path('transactions/', views.transactions, name='transactions'),

    path('transactions/edit/<int:id>/',
         views.edit_transaction,
         name='edit_transaction'),

    path('transactions/delete/<int:id>/',
         views.delete_transaction,
         name='delete_transaction'),
]