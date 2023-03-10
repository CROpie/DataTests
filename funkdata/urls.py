from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_function, name="addnew"),
    path("submitnew", views.submit_new, name="submit_new"),
    path("import", views.import_csv, name="import_csv"),
]