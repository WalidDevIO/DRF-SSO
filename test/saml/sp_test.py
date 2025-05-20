from pathlib import Path
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from samlsp import SAMLSP
from samlsp.config import Binding

from .providers import SP, IDP, CERTS_DIR

app = FastAPI()

saml = SAMLSP(SP, IDP)

@app.get("/", response_class=HTMLResponse)
async def index():
    _, html, _ = saml.get_login_request(binding=Binding.HTTP_POST)
    return html

@app.post("/saml/acs/", response_class=HTMLResponse)
async def acs(SAMLResponse: str = Form(...)):
    try:
        response = saml.parse_response(SAMLResponse)
        if response.is_valid():
            debug = f"""
                <h1>Authenticated</h1>
                <p><strong>User:</strong> {response.get_subject()}</p>
                <p><strong>Attributes:</strong></p>
                <pre>{response.get_attributes()}</pre>
                <p><strong>SessionIndex:</strong> {response.get_session_index()}</p>
                <p><strong>Conditions:</strong> {response.get_conditions()}</p>
            """
        else:
            debug = "<h1>Invalid SAML Response</h1>"
    except Exception as e:
        debug = f"<h1>Error parsing response</h1><pre>{str(e)}</pre>"

    return HTMLResponse(content=debug)

if __name__ == "__main__":
    import uvicorn
    ssl_cert = CERTS_DIR / Path("cert.pem")
    ssl_key = CERTS_DIR / Path("key.pem")
    uvicorn.run("test.saml.sp_test:app", host="0.0.0.0", port=443, ssl_keyfile=str(ssl_key), ssl_certfile=str(ssl_cert))
