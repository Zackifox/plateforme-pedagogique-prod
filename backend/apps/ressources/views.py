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
    
    def create(self, request, *args, **kwargs):   
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"ERREUR UPLOAD: {str(e)}")
            logger.error(traceback.format_exc())
            raise
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
        import requests as req
        ressource = self.get_object()
        ressource.nb_telechargements += 1
        ressource.save(update_fields=['nb_telechargements'])

        try:
            url = ressource.fichier.url
            response = req.get(url, timeout=30)
            from django.http import HttpResponse
            filename = ressource.fichier.name.split('/')[-1]
            http_response = HttpResponse(
                response.content,
                content_type='application/pdf'
            )
            http_response['Content-Disposition'] = f'attachment; filename="{filename}"'
            http_response['Access-Control-Allow-Origin'] = '*'
            return http_response
        except Exception as e:
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(ressource.fichier.url)


    @action(detail=True, methods=['get'], url_path='apercu')
    def apercu(self, request, pk=None):
        import requests as req
        ressource = self.get_object()

        try:
            url = ressource.fichier.url
            response = req.get(url, timeout=30)
            from django.http import HttpResponse
            filename = ressource.fichier.name.split('/')[-1]
            http_response = HttpResponse(
                response.content,
                content_type='application/pdf'
            )
            http_response['Content-Disposition'] = f'inline; filename="{filename}"'
            http_response['Access-Control-Allow-Origin'] = '*'
            return http_response
        except Exception as e:
            from django.http import HttpResponseRedirect
            return HttpResponseRedirect(ressource.fichier.url)