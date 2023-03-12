from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("submitnew", views.submit_new, name="submit_new"),
    path("deletelang", views.delete_language, name="deletelang"),
    path("deletetype", views.delete_function_type, name="deletetype"),
    path("deletename", views.delete_function_name, name="deletename"),
    path("modifydata", views.modify_data, name="modifydata"),
    path("import", views.import_csv, name="import_csv"),
]