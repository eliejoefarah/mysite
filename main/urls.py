from django.urls import path
from . import views

app_name = "main"
urlpatterns = [

    path("create", views.create, name="create"),
    path("add", views.add, name="add"),
    path("", views.index, name="home"),
    path("tables", views.tables, name="tables")
]
