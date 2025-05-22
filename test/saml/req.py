from .providers import SP, IDP, OUT_DIR
from samlsp.request import create_authn_request
from samlsp.config import Binding
import os

(sso_endpoint, html_auto_submit_req, req) = create_authn_request(SP, IDP, Binding.HTTP_POST)
print(sso_endpoint)

TEST_OUT = OUT_DIR / "authnreq"

if not TEST_OUT.exists():
    os.makedirs(TEST_OUT)

TEST_OUT.joinpath("post.html").write_text(html_auto_submit_req)
TEST_OUT.joinpath("request.xml").write_text(req._build_xml())
TEST_OUT.joinpath("signed.xml").write_text(req.get_request_xml())