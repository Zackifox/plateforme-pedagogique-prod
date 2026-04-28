import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('SUPERUSER_USERNAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin-uet-ucao-uut.tg@edu.com')
password = os.environ.get('SUPERUSER_PASSWORD', '+235+228@Admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password,
    )
    print(f'Superadmin "{username}" créé avec succès.')
else:
    print(f'Superadmin "{username}" existe déjà.')