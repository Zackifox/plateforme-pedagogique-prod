from django.db import models
from django.conf import settings


class Communique(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='communiques'
    )
    image = models.ImageField(upload_to='communiques/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Communiqué"
        verbose_name_plural = "Communiqués"
        ordering = ['-created_at']

    def __str__(self):
        return self.titre

    @property
    def nb_likes(self):
        return self.likes.count()

    @property
    def nb_commentaires(self):
        return self.commentaires.count()


class Commentaire(models.Model):
    communique = models.ForeignKey(
        Communique,
        on_delete=models.CASCADE,
        related_name='commentaires'
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='commentaires'
    )
    contenu = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.communique.titre}"


class Like(models.Model):
    communique = models.ForeignKey(
        Communique,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        unique_together = ('communique', 'utilisateur')

    def __str__(self):
        return f"{self.utilisateur.username} aime {self.communique.titre}"