from django.test import TestCase
from django.contrib.auth.models import User
from .models import Transaction, Budget


class UserIsolationTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )

    def test_transaction_belongs_to_correct_user(self):

        transaction = Transaction.objects.create(
            user=self.user1,
            transaction_type='income',
            amount=5000,
            description='User 1 Income',
            date='2026-09-23'
        )

        user1_transactions = Transaction.objects.filter(
            user=self.user1
        )

        user2_transactions = Transaction.objects.filter(
            user=self.user2
        )

        self.assertEqual(user1_transactions.count(), 1)
        self.assertEqual(user2_transactions.count(), 0)

        self.assertEqual(
            transaction.user,
            self.user1
        )


class BudgetIsolationTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )

        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )

    def test_budget_belongs_to_correct_user(self):

        budget = Budget.objects.create(
            user=self.user1,
            month='2026-09-01',
            amount=10000
        )

        user1_budgets = Budget.objects.filter(
            user=self.user1
        )

        user2_budgets = Budget.objects.filter(
            user=self.user2
        )

        self.assertEqual(user1_budgets.count(), 1)
        self.assertEqual(user2_budgets.count(), 0)

        self.assertEqual(
            budget.user,
            self.user1
        )
from django.urls import reverse


class AuthenticationTest(TestCase):

    def test_user_registration(self):

        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'email': 'newuser@gmail.com',
                'password': 'password123',
                'confirm_password': 'password123'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            User.objects.filter(
                username='newuser'
            ).exists()
        )

    def test_user_login(self):

        User.objects.create_user(
            username='loginuser',
            password='password123'
        )

        response = self.client.post(
            reverse('login'),
            {
                'username': 'loginuser',
                'password': 'password123'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            '_auth_user_id' in self.client.session
        )