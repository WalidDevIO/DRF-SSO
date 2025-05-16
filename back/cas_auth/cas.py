import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from core.models import CustomUser, CustomGroup
from logging import getLogger
from django.utils import timezone
from django.conf import settings
from ldap3 import Server, Connection, ALL, SUBTREE

server = Server(settings.LDAP_URI, get_info=ALL)
base_dn = settings.LDAP_BASE_DN
user_filter = settings.LDAP_USER_FILTER

logger = getLogger(__name__)

attributes = ['mail', 'givenname', 'cn', 'title', 'service', 'uid']

def get_user_from_ldap(username):
    conn = None
    user = None

    try:
        conn = Connection(server, auto_bind=True)
    except Exception as e:
        logger.error(f"Impossible d'établir la connexion avec le serveur LDAP: {e}")

    if conn:
        try:
            conn.search(base_dn, user_filter.format(username=username), attributes=attributes, search_scope=SUBTREE)
        except Exception as e:
            logger.error(f"Impossible d'effectuer la recherche sur le serveur LDAP: {e}")
    
        if conn.entries:
            user = conn.entries[0].entry_attributes_as_dict
            #TODO: Améliorer logique ici
            user["service"] = next((service[8:] for service in user["service"] if service.startswith("GENAVIR-")), None)
            if "responsable" in user["title"]:
                user["group"] = f"CDS-{user['service']}"
        
        if conn.bound:
            conn.unbind()

    return user

def populate_user(username, attributes):
    user, _ = CustomUser.objects.get_or_create(username=username)
    
    user.first_name = attributes['givenName'][0]
    user.last_name = attributes['cn'][0]
    user.email = attributes['mail'][0]
    
    group, _ = CustomGroup.objects.get_or_create(name=attributes['service'])
    if not user.group or not user.group.specific:
        user.group = group
        
    user.last_login = timezone.now()
    user.save()
    return user

def validate_ticket(ticket):
    try:
        params = {
            'ticket': ticket,
            'service': settings.CAS_SERVICE_URL
        }
        response = requests.get(settings.CAS_VALIDATE_URL, params=params, timeout=5)
        response.raise_for_status()

        root = ET.fromstring(response.text)
        ns = {'cas': 'http://www.yale.edu/tp/cas'}

        auth_success = root.find('.//cas:authenticationSuccess', ns)
        if auth_success is not None:
            user = auth_success.find('cas:user', ns).text
            return populate_user(user, get_user_from_ldap(user))
        else:
            error = root.find('.//cas:authenticationFailure', ns)
            code = error.attrib.get('code') if error is not None else "?"
            logger.error(f"[❌] Échec de validation du ticket [{code}] : {error.text if error is not None else 'Inconnu'}")
            #TODO: Rediriger vers le front en indiquant que la connexion via CAS a echoué

    except Exception as e:
        #TODO: Rediriger vers le front en indiquant qu'une erreur a eu lieu
        logger.error(f"[💥] Erreur pendant la validation du ticket : {e}")