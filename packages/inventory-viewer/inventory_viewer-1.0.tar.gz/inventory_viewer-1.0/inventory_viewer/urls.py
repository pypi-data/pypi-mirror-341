from django.urls import path
from .views import ModulyListView

urlpatterns = [
    path("", ModulyListView.as_view(), name="moduly_list"),
]
