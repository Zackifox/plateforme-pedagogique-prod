from django.core.exceptions import ValidationError
from django.conf import settings


def validate_pdf(fichier):
    # Vérifier l'extension
    if not fichier.name.lower().endswith('.pdf'):
        raise ValidationError("Seuls les fichiers PDF sont acceptés.")

    # Vérifier le type MIME via les premiers octets (magic bytes)
    header = fichier.read(5)
    fichier.seek(0)
    if header != b'%PDF-':
        raise ValidationError("Le fichier n'est pas un PDF valide.")

    # Vérifier la taille
    max_size = getattr(settings, 'PDF_MAX_SIZE', 20 * 1024 * 1024)
    if fichier.size > max_size:
        raise ValidationError(
            f"Le fichier est trop volumineux. Taille maximale : {max_size // (1024*1024)} Mo."
        )
