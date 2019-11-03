from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from foodie.orders.views import OrderViewSet, UnassignedOrderViewSet, ActiveOrderViewSet
from foodie.users.auth.views import FacebookAuthtoken
from foodie.users.views import DeliveryViewSet, ClientViewSet, NearDeliveryList

router = DefaultRouter()
router.register(r'orders/unassigned', UnassignedOrderViewSet, 'orders/unassigned')
router.register(r'orders/active', ActiveOrderViewSet, 'orders/active')
router.register(r'orders', OrderViewSet, 'orders')
router.register(r'clients', ClientViewSet, 'clients')
router.register(r'deliveries', DeliveryViewSet, 'deliveries')
router.register(r'near_deliveries', NearDeliveryList, 'near_deliveries')

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/username/', views.obtain_auth_token),
    path('token-auth/facebook/', FacebookAuthtoken.as_view()),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
