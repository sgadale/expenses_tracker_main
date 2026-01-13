from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import date

from .models import MonthlyBudget, Expense
from .forms import ExpenseForm, BudgetForm

from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def signup(request):
    form = UserCreationForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'registration/signup.html', {'form': form})


# Dashboard view
@login_required
def dashboard(request):
    selected_month = request.GET.get('month')
    expenses = Expense.objects.filter(user=request.user)

    if selected_month:
        year, month = selected_month.split('-')
        expenses = expenses.filter(date__year=year, date__month=month)

    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0

    budget = MonthlyBudget.objects.filter(user=request.user).last()
    remaining = budget.amount - total_expense if budget else 0

    category_totals = expenses.values(
        'category__name'
    ).annotate(total=Sum('amount'))

    if remaining < 0:
        messages.warning(request, "You have exceeded your budget!")

    return render(request, 'expenses/dashboard.html', {
        'expenses': expenses,
        'total_expense': total_expense,
        'budget': budget,
        'remaining': remaining,
        'selected_month': selected_month,
        'category_totals': category_totals,
        'expense_form': ExpenseForm(),
        'budget_form': BudgetForm(),
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
        messages.success(request, "Expense updated!")
        return redirect('dashboard')

    return render(request, 'expenses/expense_form.html', {
        'form': form,
        'is_edit': True
    })


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, "Expense deleted!")
        return redirect('dashboard')

    return render(request, 'expenses/confirm_delete.html', {
        'expense': expense
    })
