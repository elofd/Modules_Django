from django.urls import path
from . import views


urlpatterns = [
    path('contacts/', views.Contacts.as_view(), name='contacts_class'),
    path('about/', views.About.as_view(), name='about_class'),
    path('categories/', views.categories, name='categories'),
    path('regions/', views.Regions.as_view(), name='regions'),
    path('', views.MainPage.as_view(), name='advertisement_list'),
    path('advertisement', views.AdvertisementList.as_view(), name='advertisement_list_class')
]