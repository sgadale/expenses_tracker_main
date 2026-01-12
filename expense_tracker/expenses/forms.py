from django import forms
from .models import Expense, MonthlyBudget


class ExpenseForm(forms.ModelForm):
    class Meta: 
        model = Expense
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date'   # ✅ calendar picker
                }
            )
        }


class BudgetForm(forms.ModelForm):
    class Meta: 
        model = MonthlyBudget
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date'   # ✅ calendar picker
                }
            )
        }
