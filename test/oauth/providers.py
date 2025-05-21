import os
from dotenv import load_dotenv
from oauth import OAuth

load_dotenv(".env.local")

CONF = {
    "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth",
    "redirect_uri": "http://localhost:8000/sso/oauth/callback/",
    "scopes": ["openid", "email", "profile"],
    "client_id": os.getenv("GOOGLE_ID"),
    "client_secret": os.getenv("GOOGLE_SECRET"),
    "token_url": "https://oauth2.googleapis.com/token",
    "user_info_url": "https://openidconnect.googleapis.com/v1/userinfo"
}

OAUTH = OAuth(CONF)