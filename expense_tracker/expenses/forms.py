from django import forms
from .models import Expense, MonthlyBudget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        exclude = ['user']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'})
        }
