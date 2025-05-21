from django.urls import path
from django.contrib.auth import get_user_model
from abc import ABC, abstractmethod
from enum import Enum, auto

User = get_user_model()

class Provider(Enum):    
    OAUTH = auto()
    OIDC = auto()
    SAML = auto()
    CAS = auto()
    
class ProviderConfigurationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class AuthProvider(ABC):
    def __init__(self, title: str, name: str):
        self.title = title
        self.name = name
        self.login_view = None
        self.validate_view = None
        
    @abstractmethod
    def get_login_url(self):
        pass
    
    @abstractmethod
    def validate_response(self, request):
        pass
    
    def get_routes(self):
        return [
            path("login", self.login_view.as_view(), name=f"sso-{self.name}-login"),
            path("validate", self.validate_view.as_view(), name=f"sso-{self.name}-validate")
        ]
        
    @classmethod
    def from_config(cls, name: str, conf: dict):
        try:
            title = conf['title']
            provider = Provider[conf['type']]
            if provider == Provider.CAS:
                return CASProvider(title, name, conf)
            elif provider == Provider.SAML:
                return SAMLProvider(title, name, conf)
            elif provider == Provider.OAUTH:
                return OAuthProvider(title, name, conf)
            else:
                return OIDCProvider(title, name, conf)
        except KeyError as e:
            raise ProviderConfigurationError()
    
class CASProvider(AuthProvider):
    def __init__(self, title: str, name: str, conf: dict):
        super().__init__(title, name)
        
class SAMLProvider(AuthProvider):
    def __init__(self, title: str, name: str, conf: dict):
        super().__init__(title, name)
        
class OAuthProvider(AuthProvider):
    def __init__(self, title: str, name: str, conf: dict):
        super().__init__(title, name)
        
class OIDCProvider(AuthProvider):
    def __init__(self, title: str, name: str, conf: dict):
        super().__init__(title, name)