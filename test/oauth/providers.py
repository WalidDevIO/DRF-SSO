import os
from dotenv import load_dotenv
from drf_sso.providers.oauth import OAuth

load_dotenv(".env.local")

CONF = {
    "authorization_url": "https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize",
    "redirect_uri": "http://localhost:8000/sso/oauth/callback/",
    "scopes": ["openid", "email", "profile"],
    "client_id": os.getenv("M365_ID"),
    "client_secret": os.getenv("M365_SECRET"),
    "token_url": "https://login.microsoftonline.com/organizations/oauth2/v2.0/token",
    "user_info_url": "https://graph.microsoft.com/oidc/userinfo"
}

OAUTH = OAuth(CONF)