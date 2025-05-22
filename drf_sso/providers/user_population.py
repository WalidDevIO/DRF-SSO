from django.contrib.auth import get_user_model
from drf_sso.settings import api_settings

User = get_user_model()

(payload_lookup, db_lookup) = api_settings.BASE_USER_POPULATION['LOOKUP_FIELD']
mappings = api_settings.BASE_USER_POPULATION['MAPPINGS']

def base_user_population(payload, name):
    populate_user_conf = api_settings.PROVIDERS[name].get('populate_user_conf', None)
    if populate_user_conf is not None:
        (payload_lookup, db_lookup) = populate_user_conf['lookup_field']
        mappings = populate_user_conf['mappings']
    
    user = User.objects.get_or_create(**{db_lookup: payload[payload_lookup]})
    for payload_field, db_field in mappings.items():
        setattr(user, db_field, payload[payload_field])
    user.save()
    return user