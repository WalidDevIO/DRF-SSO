from drf_sso.providers.samlsp.config import SPConfig, IdPConfig
from drf_sso.providers.samlsp import SAMLSP as _SAMLSP
from pathlib import Path

BASE_DIR = Path("test", "saml")

OUT_DIR = BASE_DIR / "out"

OUT_DIR.mkdir(exist_ok=True, parents=True)

CONF_DIR = BASE_DIR / "conf"

CERTS_DIR = CONF_DIR / "certs"

SP = SPConfig.from_file(CONF_DIR / "sp_config.json")

IDP = IdPConfig.from_url("https://idp-notilus.ifremer.fr/idp/metadata")
SAMLSP = _SAMLSP(SP, IDP)