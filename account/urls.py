from django.urls import path
from . import views

urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name="login"),
    path('register', views.register, name="register"),
    path('user/me', views.current_user, name="current_user"),
    path('user/me/update', views.update_user, name="update_user"),
]
