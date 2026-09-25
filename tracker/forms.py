from django import forms
from django.contrib.auth.models import User
from .models import Transaction, Budget


class TransactionForm(forms.ModelForm):


    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1,
        error_messages={
            'min_value': 'Value must be greater than or equal to 1.'
        }
    )
    description = forms.CharField(
    required=True,
    error_messages={
        'required': 'Description is required.'
    }
)

    class Meta:
        model = Transaction
        fields = [
            'transaction_type',
            'category',
            'amount',
            'description',
            'date'
        ]

        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class BudgetForm(forms.ModelForm):


    month = forms.DateField(
        input_formats=['%Y-%m'],
        widget=forms.DateInput(
            attrs={'type': 'month'}
        )
    )

    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=1,
        error_messages={
            'min_value': 'Value must be greater than or equal to 1.'
        }
    )

    class Meta:
        model = Budget
        fields = ['month', 'amount']

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter password'
            }
        ),
        min_length=8
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password'
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(
            username=username
        ).exists():

            raise forms.ValidationError(
                'A user with that username already exists.'
            )

        return username

    def clean_confirm_password(self):

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get(
            'confirm_password'
        )

        if password and confirm_password:

            if password != confirm_password:

                raise forms.ValidationError(
                    'Passwords do not match.'
                )

        return confirm_password