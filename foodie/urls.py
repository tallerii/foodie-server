from django.conf.urls.static import static
from django.conf import settings

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views
from .users.views import DeliveryViewSet, ClientViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet, 'clients')
router.register(r'deliveries', DeliveryViewSet, 'deliveries')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
