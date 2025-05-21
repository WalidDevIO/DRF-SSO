from pathlib import Path
from urllib.parse import urlencode
import json

class OAuthImpl:
    def __init__(self, conf: Path|dict):
        if isinstance(conf, Path):
            with open(conf, 'r') as file:
                self._load_conf(json.load(file))
        else:
            self._load_conf(conf)
            
    def _load_conf(self, conf: dict):
        self.scopes = conf['scopes']
        self.authorization_url = conf['authorization_url']
        self.redirect_uri = conf['redirect_uri']
        self.client_id = conf['client_id']
        self.client_secret = conf['client_secret']
        self.token_url = conf['token_url']
        self.user_info_url = conf['user_info_url']
        self.extra_authorzation = conf.get('extra_authorization', None)
        
    def get_login_url(self):
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(self.scopes),
            "response_type": "code",
        }
        if self.extra_authorzation is not None:
            params.append(self.extra_authorzation)
        return f"{self.authorization_url}?{urlencode(params)}"