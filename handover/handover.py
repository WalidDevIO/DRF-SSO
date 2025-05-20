import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

def handover_from_user(user, duration=5):
    payload = {
        "exp": datetime.now().timestamp() + duration,
        "sub": user.pk
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def user_from_handover(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={
        "require": ['sub', 'exp'],
        "verify_sub": False
    })
    
    return User.objects.get(pk=payload['sub'])