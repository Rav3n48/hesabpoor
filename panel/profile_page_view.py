from django.shortcuts import render, get_object_or_404, redirect
from main.models import User
import os

from .forms import EditProfileForm, EditAvatarForm, EditPasswordForm
from main.password_hasher import hash_password, verify_password


#profile page
def profile_page(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login-page")
    
    user = get_object_or_404(User, id=user_id)

    profile_form = EditProfileForm(initial={"first_name": user.first_name, "last_name": user.last_name})
    avatar_form = EditAvatarForm()
    password_form = EditPasswordForm()


    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "avatar":
            avatar_form = EditAvatarForm(request.POST, request.FILES)
            if avatar_form.is_valid():
                old_picture = None
                if user.profile_picture:
                    old_picture = user.profile_picture.path
                user.profile_picture = avatar_form.cleaned_data["profile_picture"]
                user.save()
                if old_picture and os.path.exists(old_picture):
                    try:
                        os.remove(old_picture)
                    except:
                        pass
                return redirect("profile-page")

        elif form_type == "profile":
            profile_form = EditProfileForm(request.POST)
            if profile_form.is_valid():
                user.first_name = profile_form.cleaned_data["first_name"]
                user.last_name = profile_form.cleaned_data["last_name"]
                user.save()

                return redirect("profile-page")


        elif form_type == "password":
            password_form = EditPasswordForm(request.POST)
            if password_form.is_valid():
                current_password = password_form.cleaned_data["current_password"]
                new_password = password_form.cleaned_data["new_password"]

                if len(new_password) < 6:
                    password_form.add_error("new_password", "رمز عبور جدید باید حداقل ۶ کاراکتر باشد.")

                if verify_password(current_password, user.password):
                    user.password = hash_password(new_password)
                    user.save()

                    return redirect("profile-page")
                else:
                    password_form.add_error("current_password", "رمز عبور کنونی وارد شده اشتباه است.")


    return render(request, "panel/profile.html", {
            "user": user,
            "avatar_form": avatar_form,
            "profile_form":profile_form,
            "password_form": password_form
        })
