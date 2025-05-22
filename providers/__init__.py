from django.urls import include, path
from .auth_provider import AuthProvider
from settings import api_settings

def get_providers():
    return [
        AuthProvider.from_config(name, conf)
        for name, conf in api_settings.PROVIDERS.items()
    ]

def get_provider_urls():
    urlpatterns = []
    for provider in get_providers():
        urlpatterns.append(*provider.get_routes())
    return urlpatterns
