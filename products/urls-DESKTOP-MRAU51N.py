from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.product_list, name='products'),

    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),

    path('increase/<int:order_id>/', views.increase_quantity, name='increase'),
    path('decrease/<int:order_id>/', views.decrease_quantity, name='decrease'),
    path('remove/<int:order_id>/', views.remove_item, name='remove'),

    path('signup/', views.signup, name='signup'),

    # 🔥 LOGIN / LOGOUT ADD KAR
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='orders'),

    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_from_wishlist, name='remove_wishlist'),
    path('addresses/', views.manage_addresses, name='addresses'),
]