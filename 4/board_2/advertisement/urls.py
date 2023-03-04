from django.urls import path
from . import views


urlpatterns = [
    path('contacts/', views.Contacts.as_view(), name='contacts_class'),
    path('about/', views.About.as_view(), name='about_class'),
    path('categories/', views.categories, name='categories'),
    path('regions/', views.Regions.as_view(), name='regions'),
    path('', views.MainPage.as_view(), name='advertisement_list'),
    path('advertisement/', views.AdvertisementList.as_view(), name='advertisement_list_class'),
    path('advertisements/', views.advertisement_list, name='advertisement_list'),
    # path('groups/', views.GroupsListView.as_view(), name='groups_list'),
    path('products/', views.ProductsListView.as_view(), name='products_list'),
    path('products/create/', views.ProductCreateView.as_view(), name='create_product'),
    path('products/<int:pk>/', views.ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/confirm-archived/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/export/', views.ProductsDataExportView.as_view(), name='products_export'),
    path('orders/', views.OrdersListView.as_view(), name='orders_list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/confirm-delete/', views.OrderDeleteView.as_view(), name='order_delete'),
    path("orders/export", views.OrdersExportView.as_view(), name="orders_export"),
    path('shop/', views.ShopIndexView.as_view(), name='shop'),
]