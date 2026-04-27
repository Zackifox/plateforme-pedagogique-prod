from django.db import models


class Institut(models.Model):
    nom = models.CharField(max_length=255)
    sigle = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Institut"
        verbose_name_plural = "Instituts"
        ordering = ['nom']

    def __str__(self):
        return self.sigle or self.nom


class Filiere(models.Model):
    institut = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='filieres')
    nom = models.CharField(max_length=255)
    sigle = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom']
        unique_together = ('institut', 'nom')

    def __str__(self):
        return f"{self.institut.sigle} — {self.nom}"


class Niveau(models.Model):
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='niveaux')
    nom = models.CharField(max_length=100)
    ordre = models.PositiveSmallIntegerField(default=1, help_text="Ordre d'affichage")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['ordre', 'nom']
        unique_together = ('filiere', 'nom')

    def __str__(self):
        return f"{self.filiere} — {self.nom}"


class Matiere(models.Model):
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, related_name='matieres')
    nom = models.CharField(max_length=255)
    code = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['nom']
        unique_together = ('niveau', 'nom')

    def __str__(self):
        return f"{self.niveau} — {self.nom}"
