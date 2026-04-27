from django.db import models
from apps.catalogue.models import Matiere


def upload_to(instance, filename):
    return (
        f"ressources/"
        f"{instance.matiere.niveau.filiere.institut.sigle or instance.matiere.niveau.filiere.institut.id}/"
        f"{instance.matiere.niveau.filiere.sigle or instance.matiere.niveau.filiere.id}/"
        f"{instance.matiere.niveau.nom}/"
        f"{instance.matiere.nom}/"
        f"{filename}"
    )


class Ressource(models.Model):
    TYPE_CHOICES = [
        ('cours', 'Cours'),
        ('sujet', 'Sujet d\'examen'),
        ('td', 'Travaux dirigés'),
        ('tp', 'Travaux pratiques'),
        ('autre', 'Autre'),
    ]

    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='ressources')
    titre = models.CharField(max_length=255)
    type_ressource = models.CharField(max_length=20, choices=TYPE_CHOICES, default='cours')
    fichier = models.FileField(upload_to=upload_to)
    annee = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Année académique")
    description = models.TextField(blank=True)
    nb_telechargements = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titre} ({self.get_type_ressource_display()})"
