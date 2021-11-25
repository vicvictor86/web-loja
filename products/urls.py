from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create-product', views.create_product, name='create_product'),
    path('product-page/<int:product_id>', views.product_id, name = 'product_id')
]