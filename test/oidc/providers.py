import os
from dotenv import load_dotenv
from drf_sso.providers.oidc import OIDC as _OIDC

load_dotenv(".env.local")

config = {
    "manifest_uri": "https://login.microsoftonline.com/organizations/v2.0/.well-known/openid-configuration",
    "client_id": os.getenv("M365_ID"),
    "client_secret": os.getenv("M365_SECRET"),
    "redirect_uri": "http://localhost:8000/sso/oauth/callback/",
}

OIDC = _OIDC(config)