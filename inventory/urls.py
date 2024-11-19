

from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginUser, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('store_list/', views.store_list, name="store"),
    path('per_product/<int:pk>', views.per_product, name="per_product"),
    path('add_product/', views.add_product, name="add_product"),
    path('add_category/', views.add_category, name="add_category"),
    path('add_unit', views.add_unit, name="add_unit"),
    path('delete/<int:pk>', views.delete_product, name="delete"),
    path('update/<int:pk>', views.update_product, name="update_product"),
    path('dashboard/', views.dashboard, name="dashboard"), 

]
