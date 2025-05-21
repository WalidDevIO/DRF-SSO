from .providers import CONF
from oauth import OAuth

instance = OAuth(CONF)
print(instance.get_login_url())