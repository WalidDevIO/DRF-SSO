from .metadata import write_metadata_to_file
from .request import create_authn_request
from .config import SPConfig, IdPConfig, Binding
from .saml import SAMLSP
from pathlib import Path
import sys

test = sys.argv[1]
sp_config = SPConfig.from_file("samlsp/conf/config.json")
idp_config = IdPConfig.from_file("samlsp/conf/idp_metadata.xml")
    
def test_metadata():
    write_metadata_to_file(sp_config, Path("test/metadata.xml"))
    
def test_authreq():
    (sso_endpoint, html_auto_submit_req, req) = create_authn_request(sp_config, idp_config, Binding.HTTP_POST)
    print(sso_endpoint)
    Path("test/authnreq/authreq.html").write_text(html_auto_submit_req)
    Path("test/authnreq/authreq.xml").write_text(req._build_xml())
    Path("test/authnreq/authreq_signed.xml").write_text(req.get_request_xml())
    
if test == "all":
    test_metadata()
    test_authreq()
    
if test == "sp_metadata":
    test_metadata()
    
if test == "authreq":
    test_authreq()
    
if test == "auto_idp":
    sp = SAMLSP(sp_config=sp_config, idp_config="https://idp-notilus.ifremer.fr/idp/metadata")
    (sso_endpoint, full_link_req, req) = sp.get_login_request()
    print(sso_endpoint)
    Path("test/autoidp/authreq.xml").write_text(req._build_xml())
    Path("test/autoidp/authreq_signed.xml").write_text(req.get_request_xml())
    Path("test/autoidp/link.url").write_text(full_link_req)