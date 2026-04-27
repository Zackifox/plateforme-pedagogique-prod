from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Institut, Filiere, Niveau, Matiere
from .serializers import (
    InstitutSerializer, InstitutListSerializer,
    FiliereSerializer, FiliereListSerializer,
    NiveauSerializer, NiveauListSerializer,
    MatiereSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class InstitutViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nom', 'sigle']

    def get_queryset(self):
        return Institut.objects.annotate(nb_filieres=Count('filieres')).order_by('nom')

    def get_serializer_class(self):
        if self.action == 'list':
            return InstitutListSerializer
        return InstitutSerializer

    @action(detail=True, methods=['get'])
    def filieres(self, request, pk=None):
        institut = self.get_object()
        filieres = institut.filieres.annotate(nb_niveaux=Count('niveaux'))
        serializer = FiliereListSerializer(filieres, many=True)
        return Response(serializer.data)


class FiliereViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['institut']
    search_fields = ['nom', 'sigle']

    def get_queryset(self):
        return Filiere.objects.annotate(nb_niveaux=Count('niveaux')).order_by('nom')

    def get_serializer_class(self):
        if self.action == 'list':
            return FiliereListSerializer
        return FiliereSerializer

    @action(detail=True, methods=['get'])
    def niveaux(self, request, pk=None):
        filiere = self.get_object()
        niveaux = filiere.niveaux.annotate(nb_matieres=Count('matieres')).order_by('ordre')
        serializer = NiveauListSerializer(niveaux, many=True)
        return Response(serializer.data)


class NiveauViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['filiere']

    def get_queryset(self):
        return Niveau.objects.annotate(nb_matieres=Count('matieres')).order_by('ordre')

    def get_serializer_class(self):
        if self.action == 'list':
            return NiveauListSerializer
        return NiveauSerializer

    @action(detail=True, methods=['get'])
    def matieres(self, request, pk=None):
        niveau = self.get_object()
        matieres = niveau.matieres.annotate(
            nb_ressources=Count('ressources')
        ).order_by('nom')
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)


class MatiereViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['niveau', 'niveau__filiere', 'niveau__filiere__institut']
    search_fields = ['nom', 'code']

    def get_queryset(self):
        return Matiere.objects.annotate(nb_ressources=Count('ressources')).order_by('nom')

    def get_serializer_class(self):
        return MatiereSerializer
