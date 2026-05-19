import os
import requests
from django.core.files.storage import Storage
from django.conf import settings
from urllib.parse import quote


class SupabaseStorage(Storage):

    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL.rstrip('/')
        self.supabase_key = settings.SUPABASE_KEY
        self.bucket = settings.SUPABASE_BUCKET
        self.base_url = f"{self.supabase_url}/storage/v1"
        self.headers = {
            'Authorization': f'Bearer {self.supabase_key}',
            'apikey': self.supabase_key,
        }

    def _save(self, name, content):
        # Nettoyer le nom du fichier
        name = name.replace('\\', '/')
        url = f"{self.base_url}/object/{self.bucket}/{quote(name, safe='/')}"
        content.seek(0)
        file_content = content.read()
        headers = {
            **self.headers,
            'Content-Type': 'application/pdf',
            'x-upsert': 'true',
        }
        response = requests.post(url, headers=headers, data=file_content, timeout=60)
        if response.status_code not in [200, 201]:
            raise Exception(f"Erreur Supabase upload: {response.status_code} — {response.text}")
        return name

    def url(self, name):
        name = name.replace('\\', '/')
        supabase_url = self.supabase_url.rstrip('/')
        return f"{supabase_url}/storage/v1/object/public/{self.bucket}/{quote(name, safe='/')}"

    def exists(self, name):
        return False

    def delete(self, name):
        name = name.replace('\\', '/')
        url = f"{self.base_url}/object/{self.bucket}/{quote(name, safe='/')}"
        requests.delete(url, headers=self.headers, timeout=30)

    def _open(self, name, mode='rb'):
        name = name.replace('\\', '/')
        url = self.url(name)
        response = requests.get(url, timeout=30)
        from django.core.files.base import ContentFile
        return ContentFile(response.content)

    def size(self, name):
        return 0

    def get_available_name(self, name, max_length=None):
        return name