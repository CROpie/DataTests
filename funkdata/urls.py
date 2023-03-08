from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("testing", views.test, name="test"),
    path("import", views.import_csv, name="import_csv"),
]