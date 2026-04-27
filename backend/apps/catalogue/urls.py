from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InstitutViewSet, FiliereViewSet, NiveauViewSet, MatiereViewSet

router = DefaultRouter()
router.register('instituts', InstitutViewSet, basename='institut')
router.register('filieres', FiliereViewSet, basename='filiere')
router.register('niveaux', NiveauViewSet, basename='niveau')
router.register('matieres', MatiereViewSet, basename='matiere')

urlpatterns = [
    path('', include(router.urls)),
]
