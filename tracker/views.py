from django.shortcuts import render,redirect, get_object_or_404
from .models import Current_balance,TrackingHistory
from datetime import datetime
from django.db.models import Sum

# Create your views here.


def delete_transaction(request, id):
    if request.method == "POST":
        transaction = get_object_or_404(TrackingHistory, id=id)
        # remove the transaction
        transaction.delete()

        # recompute current balance from remaining transactions
        current_balance_obj, _ = Current_balance.objects.get_or_create(id=1)
        total = TrackingHistory.objects.aggregate(total=Sum('amount'))['total'] or 0
        current_balance_obj.balance = total
        current_balance_obj.save()

    return redirect('index')

def index(request):
    if request.method=="POST":
        description= request.POST.get('title') or ''
        amount=request.POST.get('amount')
        category=request.POST.get('category')
        created_at_str=request.POST.get('datetime')

        current_balance_obj,_=Current_balance.objects.get_or_create(id=1)
        expenses_type="CREDIT"
        amount=float(amount)
        if   amount<0:
            expenses_type="DEBIT"
        
        tracking_kwargs={
            'amount': amount,
            'expenses_type': expenses_type,
            'description': description,
            'category': category,
            'current_balance': current_balance_obj,
        }

        if created_at_str:
            try:
                # input from <input type="datetime-local"> -> 'YYYY-MM-DDTHH:MM'
                created_at_dt = datetime.fromisoformat(created_at_str)
                tracking_kwargs['created_at'] = created_at_dt
            except Exception:
                pass

        TrackingHistory.objects.create(**tracking_kwargs)
        current_balance_obj.balance += amount
        current_balance_obj.save()
        print(description,amount,expenses_type)
        print(request.POST)
        return redirect ('/')
    transactions = TrackingHistory.objects.all().order_by('-created_at')

    # Totals
    total_income = sum(t.amount for t in transactions if t.expenses_type == 'CREDIT')
    total_expense = sum(-t.amount for t in transactions if t.expenses_type == 'DEBIT')

    current_balance_obj, _ = Current_balance.objects.get_or_create(id=1)
    context = {
        'transactions': transactions,
        'current_balance': current_balance_obj.balance,
        'total_income': total_income,
        'total_expense': total_expense,
    }
    return render(request,'index.html',context)


