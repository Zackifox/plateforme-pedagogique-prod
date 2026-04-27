from rest_framework import serializers
from .models import Institut, Filiere, Niveau, Matiere


class MatiereSerializer(serializers.ModelSerializer):
    nb_ressources = serializers.IntegerField(read_only=True)

    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'code', 'description', 'niveau', 'nb_ressources']


class NiveauSerializer(serializers.ModelSerializer):
    matieres = MatiereSerializer(many=True, read_only=True)
    nb_matieres = serializers.IntegerField(read_only=True)

    class Meta:
        model = Niveau
        fields = ['id', 'nom', 'ordre', 'filiere', 'matieres', 'nb_matieres']


class NiveauListSerializer(serializers.ModelSerializer):
    nb_matieres = serializers.IntegerField(read_only=True)

    class Meta:
        model = Niveau
        fields = ['id', 'nom', 'ordre', 'nb_matieres']


class FiliereSerializer(serializers.ModelSerializer):
    niveaux = NiveauListSerializer(many=True, read_only=True)
    nb_niveaux = serializers.IntegerField(read_only=True)

    class Meta:
        model = Filiere
        fields = ['id', 'nom', 'sigle', 'description', 'institut', 'niveaux', 'nb_niveaux']


class FiliereListSerializer(serializers.ModelSerializer):
    nb_niveaux = serializers.IntegerField(read_only=True)

    class Meta:
        model = Filiere
        fields = ['id', 'nom', 'sigle', 'description', 'nb_niveaux']


class InstitutSerializer(serializers.ModelSerializer):
    filieres = FiliereListSerializer(many=True, read_only=True)
    nb_filieres = serializers.IntegerField(read_only=True)

    class Meta:
        model = Institut
        fields = ['id', 'nom', 'sigle', 'description', 'filieres', 'nb_filieres']


class InstitutListSerializer(serializers.ModelSerializer):
    nb_filieres = serializers.IntegerField(read_only=True)

    class Meta:
        model = Institut
        fields = ['id', 'nom', 'sigle', 'description', 'nb_filieres']
