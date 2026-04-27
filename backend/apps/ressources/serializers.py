from rest_framework import serializers
from .models import Ressource
from .validators import validate_pdf
from apps.catalogue.serializers import MatiereSerializer


class RessourceListSerializer(serializers.ModelSerializer):
    type_label = serializers.CharField(source='get_type_ressource_display', read_only=True)
    matiere_nom = serializers.CharField(source='matiere.nom', read_only=True)
    fichier_url = serializers.SerializerMethodField()

    class Meta:
        model = Ressource
        fields = [
            'id', 'titre', 'type_ressource', 'type_label',
            'matiere', 'matiere_nom', 'annee', 'description',
            'nb_telechargements', 'fichier_url', 'created_at',
        ]

    def get_fichier_url(self, obj):
        request = self.context.get('request')
        if obj.fichier and request:
            return request.build_absolute_uri(obj.fichier.url)
        return None


class RessourceDetailSerializer(RessourceListSerializer):
    matiere_detail = MatiereSerializer(source='matiere', read_only=True)

    class Meta(RessourceListSerializer.Meta):
        fields = RessourceListSerializer.Meta.fields + ['matiere_detail', 'updated_at']


class RessourceCreateSerializer(serializers.ModelSerializer):
    fichier = serializers.FileField(validators=[validate_pdf])

    class Meta:
        model = Ressource
        fields = [
            'id', 'titre', 'type_ressource', 'matiere',
            'annee', 'description', 'fichier',
        ]
