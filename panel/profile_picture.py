from django.shortcuts import get_object_or_404
from django.http import FileResponse
from main.models import User

def profile_picture_display(request):
    user_id = request.session.get("user_id")
    if user_id:
        user = get_object_or_404(User, id=user_id)

        path = user.profile_picture.path

        if not path:
            return None

        return FileResponse(open(path, "rb"))
    else:
        return None
