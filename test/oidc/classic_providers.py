import os
from dotenv import load_dotenv
from oidc import OIDC as _OIDC

load_dotenv(".env.local")

config = {
    "redirect_uri": "http://localhost:8000/sso/oauth/callback/",
    "manifest_uri": "https://login.microsoftonline.com/organizations/v2.0/.well-known/openid-configuration",
    "client_id": os.getenv("M365_ID"),
    "client_secret": os.getenv("M365_SECRET"),
}

OIDC = _OIDC(config)