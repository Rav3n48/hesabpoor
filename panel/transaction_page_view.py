from django.shortcuts import render, get_object_or_404, redirect
from main.models import Transaction, User


from .forms import TransactionForm


# transactions page
def transactions_page(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login-page")

    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            Transaction.objects.create(
                user_id=user,
                transaction_type=form.cleaned_data["transaction_type"],
                amount=form.cleaned_data["amount"],
                category=form.cleaned_data["category"],
                comment=form.cleaned_data["comment"],
                date=form.cleaned_data["date"]
            )

            if form.cleaned_data["transaction_type"] == "income":
                user.balance += form.cleaned_data["amount"]
                user.save()
            elif form.cleaned_data["transaction_type"] == "outcome":
                user.balance -= form.cleaned_data["amount"]
                user.save()

            return redirect("panel-page")

        return render(request, "panel/transaction.html", {
            "form": form
        })

    else:
        form = TransactionForm()
        return render(request, "panel/transaction.html", {
            "form": form
        })