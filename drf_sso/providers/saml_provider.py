from .auth_provider import AuthProvider

class SAMLProvider(AuthProvider):
    def __init__(self, title: str, name: str, conf: dict):
        super().__init__(title, name, conf.get('populate_user', 'drf_sso.providers.user_population.base_user_population'))
        self.config = conf['config']