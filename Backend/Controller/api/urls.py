from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from api.views import RawFileViewSet,ProcessedFileViewSet

# Django REST framework routes
router = routers.DefaultRouter()
router.register(r'row_files', RawFileViewSet)
router.register(r'processed_files', ProcessedFileViewSet)

urlpatterns = [
    # DRF router
    path('', include(router.urls)),
]
