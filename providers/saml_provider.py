from .auth_provider import AuthProvider

class SAMLProvider(AuthProvider):
    def __init__(self, title: str, name: str, conf: dict):
        super().__init__(title, name, conf['populate_user'])
        self.config = conf['config']