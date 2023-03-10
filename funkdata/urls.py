from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_function, name="addnew"),
    path("submitnew", views.submit_new, name="submit_new"),
    path("deletelang", views.delete_language, name="deletelang"),
    path("deletetype", views.delete_function_type, name="deletetype"),
    path("deletename", views.delete_function_name, name="deletename"),
    path("import", views.import_csv, name="import_csv"),
]