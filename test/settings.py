DRF_SSO = {
    "MODULE_BASE_URL": "http://localhost:8000/sso/",
    "FRONTEND_CALLBACK_URL": "http://localhost:8000/sso/callback/",
}

INSTALLED_APPS = [
    "drf_sso",
    "rest_framework",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
]