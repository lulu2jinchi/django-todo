from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/item_list', views.item_list, name='item_list'),
    path('api/item', views.item, name='item'),
    path('api/item/<int:id>', views.item, name='item'),
]