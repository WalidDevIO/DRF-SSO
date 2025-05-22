from samlsp.config import SPConfig, IdPConfig
from pathlib import Path

BASE_DIR = Path("test", "saml")

OUT_DIR = BASE_DIR / "out"

CONF_DIR = BASE_DIR / "conf"

CERTS_DIR = CONF_DIR / "certs"

SP = SPConfig.from_file(CONF_DIR / "sp_config.json")

IDP = IdPConfig.from_url("https://idp-notilus.ifremer.fr/idp/metadata")