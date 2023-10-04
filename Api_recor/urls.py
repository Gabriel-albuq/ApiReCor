from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.urls import include
from core.api.viewsets import ApplyModelViewSet
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'applymodel', ApplyModelViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
