from django.contrib import admin
from .models import Communique, Commentaire, Like


class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 0
    readonly_fields = ['auteur', 'contenu', 'created_at']


@admin.register(Communique)
class CommuniqueAdmin(admin.ModelAdmin):
    list_display = ['titre', 'auteur', 'nb_likes', 'nb_commentaires', 'created_at']
    search_fields = ['titre', 'contenu']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CommentaireInline]


@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ['auteur', 'communique', 'created_at']
    list_filter = ['communique']
    search_fields = ['contenu', 'auteur__username']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['utilisateur', 'communique', 'created_at']