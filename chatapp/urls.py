from django.urls import path
from .views import  VegVeganUserList
from django.urls import path

urlpatterns = [
        path('vegan-users', VegVeganUserList.as_view(), name="veg-vegan-users")

]

