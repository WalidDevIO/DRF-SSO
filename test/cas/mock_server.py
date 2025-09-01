from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
import json, traceback
from .providers import CAS

app = FastAPI()

@app.get("/", response_class=RedirectResponse)
async def index():
    return CAS.get_login_url()

@app.get("/sso/cas/", response_class=HTMLResponse)
async def acs(ticket: str):
    try:
        payload = CAS.validate_ticket(ticket)
        if payload is not None:
            debug = f"""
                <h1>Authenticated</h1>
                <p><strong>Payload:</strong></p>
                <pre>{json.dumps(payload, indent=4)}</pre>
            """
        else:
            debug = "<h1>Invalid CAS Response</h1>"
    except Exception as e:
        debug = f"<h1>Error parsing response</h1><h3>Exception: {str(e)}</h3><pre>{traceback.format_exc()}</pre>"

    return HTMLResponse(content=debug)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test.cas.mock_server:app", host="0.0.0.0", port=8000)