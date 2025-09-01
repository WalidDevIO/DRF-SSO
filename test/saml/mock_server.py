from pathlib import Path
from fastapi import FastAPI, Form
import base64
from fastapi.responses import HTMLResponse
from drf_sso.providers.samlsp.config import Binding

from .providers import SAMLSP, CERTS_DIR
import json, traceback

app = FastAPI()

def craft_cyberchef_link(saml_response: str) -> str:
    encoded_response = base64.urlsafe_b64encode(saml_response.encode('utf-8')).decode('utf-8').strip('=')
    return f"""<a href="https://cyberchef.io/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)XML_Beautify('%5C%5Ct')&input={encoded_response}" target="_blank" rel="noopener noreferrer">CyberChef View</a>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    _, html, _ = SAMLSP.get_login_request(binding=Binding.HTTP_POST)
    return html

@app.post("/saml/acs/", response_class=HTMLResponse)
async def acs(SAMLResponse: str = Form(...), RelayState: str = Form(...)):
    try:
        response = SAMLSP.parse_response(SAMLResponse, relay_state=RelayState)
        if response.is_valid():
            debug = f"""
                <h1>Authenticated</h1>
                <p><strong>User:</strong> {response.get_subject()}</p>
                <p><strong>Attributes:</strong></p>
                <pre>{json.dumps(response.get_attributes(), indent=4)}</pre>
                <p><strong>SessionIndex:</strong> {response.get_session_index()}</p>
                <p><strong>Conditions:</strong> {json.dumps(response.get_conditions(), indent=4)}</p>
                <p>SAMLResponse: {craft_cyberchef_link(SAMLResponse)}</p>
            """
        else:
            debug = f"""<h1>Invalid SAML Response</h1><p>RelayState: {RelayState}</p><p>SAMLResponse: {craft_cyberchef_link(SAMLResponse)}</p>"""
    except Exception as e:
        debug = f"<h1>Error parsing response</h1><h3>Exception: {str(e)}</h3><pre>{traceback.format_exc()}</pre>"

    return HTMLResponse(content=debug)

if __name__ == "__main__":
    import uvicorn
    ssl_cert = CERTS_DIR / Path("cert.pem")
    ssl_key = CERTS_DIR / Path("key.pem")
    uvicorn.run("test.saml.mock_server:app", host="0.0.0.0", port=443, ssl_keyfile=str(ssl_key), ssl_certfile=str(ssl_cert))
