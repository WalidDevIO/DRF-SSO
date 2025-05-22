#Django imports
from django.urls import path
from django.shortcuts import redirect

# Django Rest Framework imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# Standard library imports
from abc import ABC, abstractmethod
from enum import Enum, auto
from importlib import import_module

# Local imports
from drf_sso.handover import handover_from_user
from drf_sso.settings import api_settings
from .cas_provider import CASProvider
from .saml_provider import SAMLProvider
from .oauth_provider import OAuthProvider
from .oidc_provider import OIDCProvider

class Provider(Enum):    
    OAUTH = auto()
    OIDC = auto()
    SAML = auto()
    CAS = auto()
    
class ProviderConfigurationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def import_function(path: str):
    module_path, function_name = path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, function_name)

class AuthProvider(ABC):
    def __init__(self, title: str, name: str, populate_user: str):
        if self.__class__ == AuthProvider:
            raise TypeError("Vous ne pouvez pas instancier la classe abstraite AuthProvider")
        self.base_url = f"{api_settings.MODULE_BASE_URL}/{name}/"
        self.frontend_url = api_settings.FRONTEND_CALLBACK_URL
        self.title = title
        self.name = name
        self.populate_user = import_module(populate_user)
        
    @abstractmethod
    def get_login_url(self) -> str:
        pass
    
    @abstractmethod
    def validate_response(self, request) -> dict:
        pass

    @abstractmethod
    def populate_user(self, payload: dict):
        pass

    def get_routes(self):
        @api_view(["GET"])
        @permission_classes([AllowAny])
        def login_view(request):
            return redirect(self.get_login_url())
        
        @api_view(["GET"])
        @permission_classes([AllowAny])
        def callback_view(request):
            payload = self.validate_response(request)
            #Création/Maj utilisateurn utilisateur
            user = self.populate_user(payload)
            #Création du token de handover
            handover = handover_from_user(user)
            return redirect(f"{self.frontend_url}?handover={handover}")
        
        return [
            path(f"{self.name}/login/", login_view, name=f"sso-{self.name}-login"),
            path(f"{self.name}/callback/", callback_view, name=f"sso-{self.name}-validate")
        ]
        
    @staticmethod
    def from_config(name: str, conf: dict):
        type = conf.get('type')
        if type is None:
            raise ProviderConfigurationError("Type de provider manquant dans la configuration")
        if type.upper() not in [provider.name for provider in Provider]:
            raise ProviderConfigurationError("Type de provider inconnu dans la configuration")
        title = conf.get('title')
        if title is None:
            raise ProviderConfigurationError("Titre de provider manquant dans la configuration")
        
        provider = Provider[type.upper()]
        if provider == Provider.CAS:
            return CASProvider(title, name, conf)
        elif provider == Provider.SAML:
            return SAMLProvider(title, name, conf)
        elif provider == Provider.OAUTH:
            return OAuthProvider(title, name, conf)
        else:
            return OIDCProvider(title, name, conf)