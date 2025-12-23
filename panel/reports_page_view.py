from django.shortcuts import render, get_object_or_404, redirect
from main.models import User




# reports page  
def reports_page(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login-page")
    
    user = get_object_or_404(User, id=user_id)

    type = request.GET.get("type")

    CATEGORIES = ["salary", "food", "clothes", "transportation", 
                  "hobby", "health", "investment", "loan", "rent", "bill"]

    if type in CATEGORIES and type != "all":
        transaction = user.transactions.filter(
            category = type
        ).order_by("-date")[:50]

    else:
        transaction = user.transactions.order_by("-date")[:50]

    return render(request, "panel/reports.html", {
        "transactions": transaction,
        "type": type
    })