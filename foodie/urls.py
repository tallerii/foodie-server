from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views

from foodie.orders.views import ProductViewSet, OrderViewSet, ItemViewSet
from .users.views import DeliveryViewSet, ClientViewSet, NearDeliveryList
from .users.social_media_token.views import facebookLoginView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, 'orders')
router.register(r'items', ItemViewSet, 'items')
router.register(r'products', ProductViewSet, 'products')
router.register(r'clients', ClientViewSet, 'clients')
router.register(r'deliveries', DeliveryViewSet, 'deliveries')
router.register(r'near_deliveries', NearDeliveryList, 'near_deliveries')

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/username/', views.obtain_auth_token),
    path('token-auth/facebook/', facebookLoginView),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
