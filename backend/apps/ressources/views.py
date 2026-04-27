from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Ressource
from .serializers import (
    RessourceListSerializer,
    RessourceDetailSerializer,
    RessourceCreateSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class RessourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = [
        'matiere',
        'matiere__niveau',
        'matiere__niveau__filiere',
        'matiere__niveau__filiere__institut',
        'type_ressource',
        'annee',
    ]
    search_fields = ['titre', 'description', 'matiere__nom']
    ordering_fields = ['created_at', 'titre', 'nb_telechargements', 'annee']
    ordering = ['-created_at']

    def get_queryset(self):
        return Ressource.objects.select_related(
            'matiere__niveau__filiere__institut'
        ).all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action in ['update', 'partial_update']:
            return RessourceCreateSerializer
        if self.action == 'retrieve':
            return RessourceDetailSerializer
        return RessourceListSerializer

    @action(detail=True, methods=['get'], url_path='telecharger')
    def telecharger(self, request, pk=None):
        ressource = self.get_object()
        ressource.nb_telechargements += 1
        ressource.save(update_fields=['nb_telechargements'])

        response = FileResponse(
            ressource.fichier.open('rb'),
            content_type='application/pdf',
            as_attachment=True,
            filename=ressource.fichier.name.split('/')[-1],
        )
        return response

    @action(detail=True, methods=['get'], url_path='apercu')
    def apercu(self, request, pk=None):
        ressource = self.get_object()
        response = FileResponse(
            ressource.fichier.open('rb'),
            content_type='application/pdf',
        )
        response['Content-Disposition'] = f'inline; filename="{ressource.fichier.name.split("/")[-1]}"'
        return response
