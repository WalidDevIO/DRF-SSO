from cas import CAS as _CAS
from pathlib import Path

BASE_DIR = Path("test", "cas")

CONF_DIR = BASE_DIR / "conf"

CERTS_DIR = Path("test", "saml", "conf") / "certs"

CAS = _CAS(CONF_DIR / "cas_config.json")