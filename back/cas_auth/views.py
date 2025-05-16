from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import time
from core.models import CustomUser
from .cas import populate_user, validate_ticket

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['access_expires_in'] = refresh.access_token.payload['exp'] - int(time.time())
        data['refresh_expires_in'] = refresh.payload['exp'] - int(time.time())

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            raise PermissionDenied("Vous devez spécifier un nom d'utilisateur et un mot de passe")

        try:
            CustomUser.objects.get(username=username, specific=True)
        except CustomUser.DoesNotExist:
            raise PermissionDenied("Vous n'êtes pas autorisé a vous authentifier de cette façon")

        return super().post(request, *args, **kwargs)

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Cela génère le nouveau access_token

        # Ici, on assume que le nouveau access_token est déjà dans data, généralement sous la clé 'access'
        access_token = AccessToken(data['access'])

        # Calculer 'expires_in' en se basant sur la date d'expiration du token d'accès
        data['access_expires_in'] = access_token.payload['exp'] - int(time.time())
        # Optionnel : Si ROTATE_REFRESH_TOKENS est activé et vous voulez aussi renvoyer le refresh_expires_in
        if 'refresh' in data:
            refresh_token = RefreshToken(data['refresh'])  # Utilisez RefreshToken si c'est un refresh token
            data['refresh_expires_in'] = refresh_token.payload['exp'] - int(time.time())

        return data

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class CASAuthCallback(APIView):
    def get(self, request, *args, **kwargs):
        ticket = request.query_params.get('ticket', None)
        if ticket is None:
            raise Exception("Pas de ticket")
        attributes = validate_ticket(ticket=ticket)
        if attributes is None:
            raise Exception("Ticket invalide")
        user = populate_user(attributes[0], attributes[1])
        return Response({
            "user": user.username,
            "name": f"{user.last_name.upper()} {user.first_name}",
            "service": user.group.name
        })