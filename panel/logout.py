from django.shortcuts import redirect


def logout(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login-page")
    
    else:
        del request.session["user_id"]
        return redirect("main-page")