import os
from dotenv import load_dotenv
from odic import ODIC as _ODIC

load_dotenv(".env.local")

CONF = {
    "manifest_uri": "https://login.microsoftonline.com/organizations/v2.0/.well-known/openid-configuration",
    "redirect_uri": "http://localhost:8000/sso/oauth/callback/",
    "client_id": os.getenv("M365_ID"),
    "client_secret": os.getenv("M365_SECRET"),
}

ODIC = _ODIC(CONF)