from django.shortcuts import render, get_object_or_404, redirect
from main.models import User
from .forms import FinancialTargetForm

def financial_target_page(request):
    user_id = request.session.get("user_id")
    if user_id:
        user = get_object_or_404(User, id=user_id)
        if request.method == "POST":
            form = FinancialTargetForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data["financial_target_text"]
                targets = user.financial_targets
                targets.append(text)
                user.financial_targets = targets
                user.save()
                return redirect("panel-page")
            else:
                return render(request, "panel/financial_target.html", {"form": form})

        if request.method == "GET":
            form = FinancialTargetForm()
            return render(request, "panel/financial_target.html", {"form": form})
    else:
        return redirect("login-page")

    