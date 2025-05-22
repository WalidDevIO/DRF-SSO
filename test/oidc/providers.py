import os
from dotenv import load_dotenv
from providers import AuthProvider

load_dotenv(".env.local")

config = {
    "type": "OIDC",
    "title": "Microsoft 365",
    "config": {
        "manifest_uri": "https://login.microsoftonline.com/organizations/v2.0/.well-known/openid-configuration",
        "client_id": os.getenv("M365_ID"),
        "client_secret": os.getenv("M365_SECRET"),
    }
}

OIDC = AuthProvider.from_config("oauth", config)