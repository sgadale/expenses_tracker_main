from django import forms
from .models import Expense, MonthlyBudget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }



class BudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        exclude = ['user']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['month'].input_formats = ['%Y-%m']
