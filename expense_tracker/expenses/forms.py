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
            'month': forms.DateInput(
                attrs={'type': 'month'},
                format='%Y-%m'          # ✅ IMPORTANT
            )
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['month'].input_formats = ['%Y-%m']