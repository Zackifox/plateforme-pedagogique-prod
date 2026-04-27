from rest_framework import serializers
from .models import Communique, Commentaire, Like
from django.contrib.auth import get_user_model

User = get_user_model()


class AuteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentaireSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(read_only=True)

    class Meta:
        model = Commentaire
        fields = ['id', 'auteur', 'contenu', 'created_at']
        read_only_fields = ['id', 'auteur', 'created_at']


class CommuniqueListSerializer(serializers.ModelSerializer):
    auteur = AuteurSerializer(read_only=True)
    nb_likes = serializers.IntegerField(read_only=True)
    nb_commentaires = serializers.IntegerField(read_only=True)
    utilisateur_a_like = serializers.SerializerMethodField()

    class Meta:
        model = Communique
        fields = [
            'id', 'titre', 'contenu', 'auteur', 'image',
            'nb_likes', 'nb_commentaires', 'utilisateur_a_like',
            'created_at', 'updated_at',
        ]

    def get_utilisateur_a_like(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(utilisateur=request.user).exists()
        return False


class CommuniqueDetailSerializer(CommuniqueListSerializer):
    commentaires = CommentaireSerializer(many=True, read_only=True)

    class Meta(CommuniqueListSerializer.Meta):
        fields = CommuniqueListSerializer.Meta.fields + ['commentaires']


class CommuniqueCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communique
        fields = ['id', 'titre', 'contenu', 'image']