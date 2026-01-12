from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import MonthlyBudget, Expense
from .forms import ExpenseForm, BudgetForm

# Create your views here.
# Dashboard view
@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    total_expense = expenses.aggregate(
        total=Sum('amount'))['total'] or 0
    budget = MonthlyBudget.objects.filter(user=request.user).last()

    remaining = budget.amount - total_expense if budget else 0

    if remaining < 0:
        messages.warning(request, 'You have exceeded your monthly budget!')

    return render(
        request, 'expenses/dashboard.html',
        {
            'expenses': expenses,
            'totoal_expenses': total_expense,
            'budget': budget,
            'remaining': remaining 
        })

# Add expense
@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)

    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, 'Expense added!')
        return redirect('dashboard')
    
    return render(request, 'expenses/expense_form.html', {'form': form})
    
# set budget
@login_required
def set_budget(request):
    form = BudgetForm(request.POST or None)

    if form.is_valid():
        budget = form.save(commit=False)
        budget.user = request.user
        budget.save()
        messages.success(request, "Budget saved!")
        return redirect('dashboard')
    
    return render(request, 'expenses/budget_form.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)

    if form.is_valid():
        form.save()
        messages.success(request, "Expense updated successfully")
        return redirect('dashboard')

    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'is_edit': True
    })
