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
        if not obj.fichier:
            return None
        url = obj.fichier.url
        # Forcer le type fl_attachment pour le téléchargement correct
        if 'cloudinary.com' in url:
            # Remplacer /raw/upload/ par /raw/upload/fl_attachment/
            url = url.replace('/raw/upload/', '/raw/upload/fl_attachment/')
            return url
    fichier_url = serializers.SerializerMethodField()
    apercu_url = serializers.SerializerMethodField()

    def get_apercu_url(self, obj):
        if not obj.fichier:
            return None
        url = obj.fichier.url
        # URL simple sans fl_attachment pour l'aperçu inline
        return url


class RessourceDetailSerializer(RessourceListSerializer):
    matiere_detail = MatiereSerializer(source='matiere', read_only=True)

    class Meta(RessourceListSerializer.Meta):
        fields = RessourceListSerializer.Meta.fields + ['matiere_detail', 'updated_at']


class RessourceCreateSerializer(serializers.ModelSerializer):
    fichier = serializers.FileField(validators=[validate_pdf])

    class Meta:
        model = Ressource
        fields = [
            'id', 'titre', 'type_ressource', 'type_label',
            'matiere', 'matiere_nom', 'annee', 'description',
            'nb_telechargements', 'fichier_url', 'apercu_url', 'created_at',
        ]
