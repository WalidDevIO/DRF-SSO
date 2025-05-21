from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import json
from .providers import CERTS_DIR, CAS

app = FastAPI()

@app.get("/", response_class=RedirectResponse)
async def index():
    return CAS.get_login_url()

@app.get("/sso/cas/", response_class=HTMLResponse)
async def acs(ticket: str):
    try:
        (username, attributes) = CAS.validate_ticket(ticket)
        if username is not None:
            debug = f"""
                <h1>Authenticated</h1>
                <p><strong>User:</strong> {username}</p>
                <p><strong>Attributes:</strong></p>
                <pre>{json.dumps(attributes, indent=4)}</pre>
            """
        else:
            debug = "<h1>Invalid CAS Response</h1>"
    except Exception as e:
        debug = f"<h1>Error parsing response</h1><pre>{str(e)}</pre>"

    return HTMLResponse(content=debug)

if __name__ == "__main__":
    import uvicorn
    ssl_cert = CERTS_DIR / Path("cert.pem")
    ssl_key = CERTS_DIR / Path("key.pem")
    uvicorn.run("test.cas.mock_server:app", host="0.0.0.0", port=443, ssl_keyfile=str(ssl_key), ssl_certfile=str(ssl_cert))
