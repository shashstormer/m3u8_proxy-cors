import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from cors import add_cors

try:
    enable_docs = bool(os.getenv("documentation", False))
    docs_url = os.getenv('docs_url', '/docs') if enable_docs and os.getenv('docs_url', '/docs') else None
    redoc_url = os.getenv('redoc_url', '/redoc') if enable_docs and os.getenv('redoc_url', '/redoc') else None
    # set environment variable 'documentation' to 'True' if you want to enable the /docs path
except TypeError:
    enable_docs = False
    docs_url = '/docs' if enable_docs else None
    redoc_url = '/redoc' if enable_docs else None

allow_no_url_param_also = os.getenv("no_url_param", "false")
allow_no_url_param_also = allow_no_url_param_also == "true"


app = FastAPI(openapi_url=None, docs_url=docs_url, redoc_url=redoc_url)
default_port = "5010"

if enable_docs:
    @app.get('/')
    async def home(_: Request):
        return RedirectResponse('/docs')


allowed_origins = os.getenv("origins", "*")
# You may set your environment variable with the domains you want to allow requests from(your site)
# You may put ',' between the domains if you have multiple domains

try:
    port = int(float(os.getenv("port", default_port)))
except TypeError:
    port = int(default_port)
# You don't need to change anything here unless you want to run it on a different or specific port
# to run on a different port you can set the port env variable

add_cors(app, allowed_origins, allow_no_url_param_also)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=port)
