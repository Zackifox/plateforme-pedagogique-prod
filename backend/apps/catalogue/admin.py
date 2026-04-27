from django.contrib import admin
from .models import Institut, Filiere, Niveau, Matiere


class FiliereInline(admin.TabularInline):
    model = Filiere
    extra = 0


class NiveauInline(admin.TabularInline):
    model = Niveau
    extra = 0


class MatiereInline(admin.TabularInline):
    model = Matiere
    extra = 0


@admin.register(Institut)
class InstitutAdmin(admin.ModelAdmin):
    list_display = ['nom', 'sigle', 'created_at']
    search_fields = ['nom', 'sigle']
    inlines = [FiliereInline]


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'sigle', 'institut']
    list_filter = ['institut']
    search_fields = ['nom', 'sigle']
    inlines = [NiveauInline]


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ['nom', 'filiere', 'ordre']
    list_filter = ['filiere__institut', 'filiere']
    inlines = [MatiereInline]


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['nom', 'code', 'niveau']
    list_filter = ['niveau__filiere__institut', 'niveau__filiere', 'niveau']
    search_fields = ['nom', 'code']
