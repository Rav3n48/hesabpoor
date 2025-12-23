from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from main.models import User
from django.utils import timezone
from datetime import timedelta



# the main panel page
def panel_page(request):
    if request.method == "GET":
        user_id = request.session.get("user_id")
        if user_id:
            user = get_object_or_404(User, id=user_id)

            remove_ft_index = request.GET.get("rm_ft")
            if remove_ft_index:
                try:
                    targets = user.financial_targets
                    targets.pop(int(remove_ft_index))
                    user.financial_targets = targets
                    user.save()
                except:
                    request.session["notification_code"] = 9
                    return redirect("notification-page")
                    #pass
            
            range_type = request.GET.get("range", "all")
            today = timezone.now().date()

            # all time balance
            incomes_total = user.transactions.filter(transaction_type="income").aggregate(sum=Sum("amount"))["sum"] or 0
            outcomes_total = user.transactions.filter(transaction_type="outcome").aggregate(sum=Sum("amount"))["sum"] or 0
            balance = incomes_total - outcomes_total

            financial_targets = user.financial_targets

            if range_type == "this-week":
                start_week = today - timedelta(days=today.weekday())
                end_week = start_week + timedelta(days=6)
                transactions = user.transactions.filter(
                    date__range=(start_week, end_week)
                )

            elif range_type == "this-month":
                transactions = user.transactions.filter(
                    date__year=today.year,
                    date__month=today.month
                )

            elif range_type == "last-month":
                last_month = today.replace(day=1) - timedelta(days=1)
                transactions = user.transactions.filter(
                    date__year=last_month.year,
                    date__month=last_month.month
                )
            
            elif range_type == "this-year":
                transactions = user.transactions.filter(
                    date__year=today.year
                )

            else:
                transactions = user.transactions.all()

            # selected time
            incomes = transactions.filter(transaction_type="income")
            outcomes = transactions.filter(transaction_type="outcome")
            total_incomes = incomes.aggregate(sum=Sum("amount"))["sum"] or 0
            total_outcomes = outcomes.aggregate(sum=Sum("amount"))["sum"] or 0

            return render(request, "panel/index.html", {
                "user": user,
                "balance": balance,
                "incomes_total": total_incomes,
                "outcomes_total": total_outcomes,
                "transactions": transactions,
                "range_type": range_type,
                "financial_targets": financial_targets
            })
        else:
            return redirect("login-page")