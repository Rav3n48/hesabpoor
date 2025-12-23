"""
URL configuration for hesabpoor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('l0g1n_Adm1n_h3sabp00r/', admin.site.urls),
    #main routes
    path("", include("main.urls")),
    #panel routes
    path("panel/", include("panel.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)