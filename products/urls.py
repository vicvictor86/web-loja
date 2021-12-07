from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create-product', views.create_product, name='create_product'),
    path('edit-product/<int:product_id>', views.edit_product, name = 'edit_product'),
    path('update-product', views.update_product, name = 'update_product'),
    path('product-page/<int:product_id>', views.product_page, name = 'product_page'),
    path('product-page/buy-product/<int:product_id>&<int:quantity>', views.buy_product, name = 'buy_product'),
    path('confirmed_purchase/<int:product_id>&<int:user_id>', views.confirmed_purchase, name = 'confirmed_purchase'),
    path('cancel_purchase/<int:product_id>', views.cancel_purchase, name='cancel_purchase'),
    path('cart/<int:product_id>&<int:user_id>', views.add_cart, name = 'add_cart'),
    path('cart-view/<int:user_id>', views.products_in_cart, name='products_in_cart'),
    path('delete-cart/<int:product_id>&<int:user_id>', views.delete_cart_product, name='delete_cart_product'),
]