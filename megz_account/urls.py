"""megz_account URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from megz_account_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"),
    path("accounts", views.accounts, name="accounts"),
    path("accounts/<int:month>/<int:date>/<int:year>", views.accountList, name="accounts"),
    path("getAmt", views.get_amt, name="getAmt"),
    path("signup", views.signup, name="signup"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("signin", views.signin, name="signin"),
    path("", include("allauth.urls")),
    path("signout", views.signout, name="signout"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)