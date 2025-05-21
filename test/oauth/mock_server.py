from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from .providers import OAUTH
import json, base64, traceback

app = FastAPI()

@app.get("/", response_class=RedirectResponse)
async def index():
    return OAUTH.get_login_url()

@app.get("/sso/oauth/callback/", response_class=HTMLResponse)
async def oauth(code: str):
    try:
        res1 = OAUTH.exchange_code(code)
        res2 = OAUTH.get_userinfo(res1['access_token'])
        id_jwt_b64 = (res1['id_token'].split(".")[1])
        id_jwt_str = base64.b64decode(id_jwt_b64+"===").decode()
        id_jwt_json = json.loads(id_jwt_str)
        debug = f"""
            <h1>Authenticated</h1>
            <p><strong>Response from code/token exchange :</strong></p>
            <pre>{json.dumps(res1, indent=4)}</pre>
            <p><strong>Response from userinfo endpoint :</strong></p>
            <pre>{res2}</pre>
            <p><strong>JWT OIDC Content</strong></p>
            <pre>{json.dumps(id_jwt_json, indent=4)}</pre>
        """
    except Exception as e:
        debug = f"<h1>Error parsing response</h1><h3>Exception: {str(e)}</h3><pre>{traceback.format_exc()}</pre>"
    return HTMLResponse(content=debug)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test.oauth.mock_server:app", host="0.0.0.0", port=8000)