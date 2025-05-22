from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from .providers import OIDC
import json, traceback

app = FastAPI()

@app.get("/", response_class=RedirectResponse)
async def index():
    return OIDC.get_login_url()

@app.get("/sso/oauth/callback/", response_class=HTMLResponse)
async def oauth(code: str):
    try:
        payload = OIDC.get_id_token(code)
        debug = f"""
            <h1>Authenticated</h1>
            <p><strong>ID TOKEN :</strong></p>
            <pre>{json.dumps(payload, indent=4)}</pre>
        """
    except Exception as e:
        debug = f"<h1>Error parsing response</h1><h3>Exception: {str(e)}</h3><pre>{traceback.format_exc()}</pre>"
    return HTMLResponse(content=debug)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test.oidc.mock_server:app", host="0.0.0.0", port=8000)