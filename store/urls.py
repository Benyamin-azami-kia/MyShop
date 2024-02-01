from django.urls import path
from . import views
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router=DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers',views.CustomerViewSet)

product_router=NestedDefaultRouter(router,'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

cart_router=NestedDefaultRouter(router,'carts', lookup='cart')
cart_router.register('items',views.CartItemViewSet, basename='cart-items')

urlpatterns= router.urls + product_router.urls + cart_router.urls
