from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .serializers import CustomTokenObtainPairSerializer, AdminUserSerializer, InscriptionSerializer

User = get_user_model()

GOOGLE_CLIENT_ID = '727006221568-rkhqg3n96j78gla1oreqggqge3eodo3p.apps.googleusercontent.com'


def generer_tokens(user):
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    access['username'] = user.username
    access['is_admin'] = getattr(user, 'is_admin', False)
    access['is_superuser'] = user.is_superuser
    return {
        'access': str(access),
        'refresh': str(refresh),
        'username': user.username,
        'email': user.email,
    }


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class InscriptionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = InscriptionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(generer_tokens(user), status=201)
        return Response(serializer.errors, status=400)


class LoginEmailOuUsernameView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifiant = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not identifiant or not password:
            return Response({'detail': 'Identifiant et mot de passe requis.'}, status=400)

        user = None
        if '@' in identifiant:
            try:
                user = User.objects.get(email__iexact=identifiant)
            except User.DoesNotExist:
                pass
        else:
            try:
                user = User.objects.get(username__iexact=identifiant)
            except User.DoesNotExist:
                pass

        if user is None or not user.check_password(password):
            return Response({'detail': 'Identifiants incorrects.'}, status=401)

        if not user.is_active:
            return Response({'detail': 'Compte désactivé.'}, status=403)

        return Response(generer_tokens(user))


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'detail': 'Token Google manquant.'}, status=400)

        try:
            # Récupérer les infos utilisateur via l'access_token
            import requests as req
            resp = req.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10,
            )
            if resp.status_code != 200:
                return Response({'detail': 'Token Google invalide.'}, status=400)
            infos = resp.json()
        except Exception as e:
            return Response({'detail': f'Erreur Google : {str(e)}'}, status=400)

        email = infos.get('email')
        prenom = infos.get('given_name', '')
        nom = infos.get('family_name', '')

        if not email:
            return Response({'detail': 'Email non fourni par Google.'}, status=400)

        user, created = User.objects.get_or_create(
            email__iexact=email,
            defaults={
                'username': _generer_username(email, prenom, nom),
                'email': email.lower(),
                'first_name': prenom,
                'last_name': nom,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        return Response({**generer_tokens(user), 'nouveau': created})


def _generer_username(email, prenom, nom):
    base = prenom.lower() if prenom else email.split('@')[0]
    base = ''.join(c for c in base if c.isalnum())
    username = base
    compteur = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}{compteur}"
        compteur += 1
    return username


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Déconnexion réussie.'})
        except Exception:
            return Response({'detail': 'Token invalide.'}, status=400)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AdminUserSerializer(request.user)
        return Response(serializer.data)