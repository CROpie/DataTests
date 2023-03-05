from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new_beer", views.addbeer, name="new"),
    path("show_beer", views.showbeer, name="showbeer"),
    path("submit_beer", views.submitbeer, name="submitbeer"),
]