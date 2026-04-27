from django.contrib import admin
from .models import Ressource


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_ressource', 'matiere', 'annee', 'nb_telechargements', 'created_at']
    list_filter = [
        'type_ressource',
        'matiere__niveau__filiere__institut',
        'matiere__niveau__filiere',
        'matiere__niveau',
        'annee',
    ]
    search_fields = ['titre', 'matiere__nom']
    readonly_fields = ['nb_telechargements', 'created_at', 'updated_at']
