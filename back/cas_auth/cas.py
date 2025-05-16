import requests
import xml.etree.ElementTree as ET
from django.conf import settings
from core.models import CustomUser, CustomGroup
from logging import getLogger
from django.utils import timezone

logger = getLogger(__name__)

def populate_user(username, attributes):
    user, _ = CustomUser.objects.get_or_create(username=username)
    
    user.first_name = attributes['givenname']
    user.last_name = attributes['cn']
    user.email = attributes['mail']
    
    group, _ = CustomGroup.objects.get_or_create(name=attributes['service'])
    if not user.group or not user.group.specific:
        user.group = group
        
    user.last_login = timezone.now()
    user.save()
    return user

def validate_ticket(ticket):
    attributes_dict = {}
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
            attributes = auth_success.find('cas:attributes', ns)
            if attributes is not None:
                is_cds = False
                for attr in attributes:
                    tag = attr.tag.split('}')[-1]
                    if tag in ['givenname', 'cn', 'mail']:
                        attributes_dict[tag] = attr.text
                        
                    if tag == "service" and attr.text.startswith("GENAVIR-"):
                        attributes_dict['service'] = attr.text[8:]
                        
                    if tag == "title" and "responsable" in attr.text:
                        is_cds = True
                        
                if is_cds:
                    attributes_dict['service'] = f"CDS-{attributes_dict['service']}"
                    
                return (user, attributes_dict)
        else:
            error = root.find('.//cas:authenticationFailure', ns)
            code = error.attrib.get('code') if error is not None else "?"
            logger.error(f"[❌] Échec de validation du ticket [{code}] : {error.text if error is not None else 'Inconnu'}")
            #TODO: Rediriger vers le front en indiquant que la connexion via CAS a echoué

    except Exception as e:
        #TODO: Rediriger vers le front en indiquant qu'une erreur a eu lieu
        logger.error(f"[💥] Erreur pendant la validation du ticket : {e}")