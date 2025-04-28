from django.urls import path
from .views import VegVeganUserList
from django.urls import path, include

urlpatterns = [
        path('vegan-users', VegVeganUserList.as_view(), name="veg-vegan-users"),

]

