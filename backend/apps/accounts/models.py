from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    institut = models.ForeignKey(
        'catalogue.Institut',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='admins',
        help_text="Institut géré par cet administrateur (vide = super admin)"
    )

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username
