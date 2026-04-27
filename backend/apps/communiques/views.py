from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Communique, Commentaire, Like
from .serializers import (
    CommuniqueListSerializer,
    CommuniqueDetailSerializer,
    CommuniqueCreateSerializer,
    CommentaireSerializer,
)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class CommuniqueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['titre', 'contenu']
    ordering = ['-created_at']

    def get_queryset(self):
        return Communique.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create' or self.action in ['update', 'partial_update']:
            return CommuniqueCreateSerializer
        if self.action == 'retrieve':
            return CommuniqueDetailSerializer
        return CommuniqueListSerializer

    def perform_create(self, serializer):
        serializer.save(auteur=self.request.user)

    # ── Liker / Déliker ──
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def liker(self, request, pk=None):
        communique = self.get_object()
        like, created = Like.objects.get_or_create(
            communique=communique,
            utilisateur=request.user,
        )
        if not created:
            like.delete()
            return Response({'liked': False, 'nb_likes': communique.likes.count()})
        return Response({'liked': True, 'nb_likes': communique.likes.count()})

    # ── Commenter ──
    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def commenter(self, request, pk=None):
        communique = self.get_object()
        if request.method == 'GET':
            commentaires = communique.commentaires.select_related('auteur').all()
            serializer = CommentaireSerializer(commentaires, many=True)
            return Response(serializer.data)

        if not request.user.is_authenticated:
            return Response({'detail': 'Connexion requise.'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(communique=communique, auteur=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ── Supprimer un commentaire ──
    @action(
        detail=True,
        methods=['delete'],
        url_path='commenter/(?P<commentaire_id>[^/.]+)',
        permission_classes=[permissions.IsAuthenticated],
    )
    def supprimer_commentaire(self, request, pk=None, commentaire_id=None):
        try:
            commentaire = Commentaire.objects.get(
                id=commentaire_id,
                communique_id=pk,
            )
        except Commentaire.DoesNotExist:
            return Response({'detail': 'Commentaire introuvable.'}, status=404)

        if commentaire.auteur != request.user and not request.user.is_superuser:
            return Response({'detail': 'Non autorisé.'}, status=403)

        commentaire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)