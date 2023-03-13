from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("submitnew", views.submitNew, name="submit_new"),
    path("deletedata", views.deleteData, name="deletedata"),
    path("modifydata", views.modifyData, name="modifydata"),
    path("import", views.import_csv, name="import_csv"),
]