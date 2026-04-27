from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommuniqueViewSet

router = DefaultRouter()
router.register('', CommuniqueViewSet, basename='communique')

urlpatterns = [
    path('', include(router.urls)),
]