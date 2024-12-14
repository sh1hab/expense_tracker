
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Expense, Category
from .forms import ExpenseForm
from django.db.models.functions import TruncMonth
import json


@login_required
def dashboard(request):
    
    expenses = Expense.objects.filter(user=request.user)
        
    # Today's expenses
    today = timezone.now().date()
    daily_expenses = expenses.filter(date=today)
    daily_total = daily_expenses.aggregate(
            total=Sum('amount', default=0)
    )['total']
        
    # This month's expenses
    monthly_expenses = expenses.filter(
            date__year=today.year, 
            date__month=today.month
    )
    monthly_total = monthly_expenses.aggregate(
            total=Sum('amount', default=0)
    )['total']
        
    # This year's expenses
    yearly_expenses = expenses.filter(
            date__year=today.year
    )
    yearly_total = yearly_expenses.aggregate(
            total=Sum('amount', default=0)
    )['total']
        
    context = {
        'daily_total': daily_total,
        'monthly_total': monthly_total,
        'yearly_total': yearly_total,
        'expenses': expenses,
        # 'monthly_expenses': monthly_expenses,
        # 'yearly_expenses': yearly_expenses,
    }

    return render(request, 'dashboard.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.category = form.cleaned_data.get('category')
            expense.save()
            return redirect('expenses:dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expense_form.html', {'form': form})

@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expenses:dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expense_form.html', {'form': form})

@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('expenses:dashboard')

@login_required
def analytics(request):
    monthly_category_spending = Expense.objects.filter(
        user=request.user,
        date__year=timezone.now().year,
        date__month=timezone.now().month
    ).values('category__name').annotate(
        total_amount=Sum('amount')
    ).order_by('-total_amount')

    # Prepare data for Chart.js
    category_labels = [item['category__name'] for item in monthly_category_spending]
    category_amounts = [float(item['total_amount']) for item in monthly_category_spending]

    # Weekly spending trends
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)
    
    weekly_spending = Expense.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).values('date').annotate(
        daily_total=Sum('amount')
    ).order_by('date')

    # Prepare weekly spending data
    weekly_labels = [item['date'].strftime('%Y-%m-%d') for item in weekly_spending]
    weekly_amounts = [float(item['daily_total']) for item in weekly_spending]

    context = {
        'category_labels': json.dumps(category_labels),
        'category_amounts': json.dumps(category_amounts),
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_amounts': json.dumps(weekly_amounts),
    }
    
    return render(request, 'analytics.html', context)