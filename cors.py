import json
import os
from fastapi import Request, Response
from request_helper import Requester


async def cors(request: Request, origins) -> Response:
    if not request.query_params.get('url'):
        return Response()
    file_type = request.query_params.get('type')
    requested = Requester(str(request.url))
    main_url = requested.host + requested.path + "?url="
    url = requested.query_params.get("url")
    requested = Requester(url)
    headers_to_give = request.headers.mutablecopy()
    headers_to_give.update(json.loads(request.query_params.get("headers", "{}").replace("'", '"')))
    content, headers, code, cookies = requested.get(
        data=None,
        headers=headers_to_give,
        method=request.query_params.get("method", "GET"),
        json_data=json.loads(request.query_params.get("json", "{}")),
        additional_params=json.loads(request.get('params', '{}'))
    )
    headers['Access-Control-Allow-Origin'] = origins
    # if "text/html" not in headers.get('Content-Type'):
    #     headers['Content-Disposition'] = 'attachment; filename="master.m3u8"'
    del_keys = [
        # 'Vary',
        # 'Server',
        # 'Report-To',
        # 'NEL',
        'Content-Encoding',
        'Transfer-Encoding',
        'Content-Length',
        # "Content-Type"
    ]
    for key in del_keys:
        headers.pop(key, None)

    if (file_type == "m3u8" or "m3u8" in url) and code != 404:
        content = content.decode("utf-8")
        new_content = ""
        for line in content.split("\n"):
            if line.startswith("#"):
                new_content += line
            elif line.startswith('/'):
                new_content += main_url + requested.safe_sub(requested.host + line)
            elif line.startswith('http'):
                new_content += main_url + requested.safe_sub(line)
            elif line.strip(' '):
                new_content += main_url + requested.safe_sub(
                    requested.host +
                    '/'.join(str(requested.path).split('?')[0].split('/')[:-1]) +
                    '/' +
                    requested.safe_sub(line)
                )
            new_content += "\n"
        content = new_content
    if "location" in headers:
        if headers["location"].startswith("/"):
            headers["location"] = requested.host + headers["location"]
        headers["location"] = main_url+headers["location"]
    return Response(content, code, headers=headers)


def add_cors(app, origins):
    cors_path = os.getenv('cors_url', '/cors')

    @app.get(cors_path)
    async def cors_caller(request: Request) -> Response:
        return await cors(request, origins=origins)
