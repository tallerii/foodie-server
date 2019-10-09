from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views

from foodie.orders.views import ProductViewSet, OrderViewSet, ItemViewSet
from .users.views import DeliveryViewSet, ClientViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, 'orders')
router.register(r'items', ItemViewSet, 'items')
router.register(r'products', ProductViewSet, 'products')
router.register(r'clients', ClientViewSet, 'clients')
router.register(r'deliveries', DeliveryViewSet, 'deliveries')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
