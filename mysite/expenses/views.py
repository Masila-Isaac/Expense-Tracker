from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm

def index(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = sum(t.amount for t in transactions if t.transaction_type == 'IN')
    total_expense = sum(t.amount for t in transactions if t.transaction_type == 'EX')
    balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'expenses/index.html', context)

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('index')
    else:
        form = TransactionForm()

    return render(request, 'expenses/add_transaction.html', {'form': form})
