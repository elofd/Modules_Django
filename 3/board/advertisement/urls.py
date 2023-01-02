from django.urls import path
from . import views


urlpatterns = [
    path("", views.advertisement_list, name="advertisement_list"),
    path("advertisement/", views.advertisement_detail, name="advertisement_list"),
    path("advertisement-python-part-1/", views.advertisement_python_part_1, name="advertisement_python_part_1"),
    path("advertisement-python-part-2/", views.advertisement_python_part_2, name="advertisement_python_part_2"),
    path("advertisement-python-django/", views.advertisement_python_django, name="advertisement_python_django"),
    path("advertisement-python-advanced/", views.advertisement_python_advanced, name="advertisement_python_advanced"),
    path("advertisement-web-layout/", views.advertisement_web_layout, name="advertisement_web_layout"),
]