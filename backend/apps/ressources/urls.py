from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RessourceViewSet

router = DefaultRouter()
router.register('', RessourceViewSet, basename='ressource')

urlpatterns = [
    path('', include(router.urls)),
]
