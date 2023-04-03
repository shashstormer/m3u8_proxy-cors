import json
import aiohttp
import multidict
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse

app = FastAPI()


async def home(request: Request) -> Response:
    return RedirectResponse("/docs")


@app.get('/cors')
async def handle(request: Request):
    headers_ = request.query_params.get('headers',
                                        "{\"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36}\"}")
    headers_ = json.loads(headers_)
    headers_["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36}"
    async with aiohttp.ClientSession(headers=multidict.CIMultiDict(headers_)) as session:
        url = request.query_params.get('url')
        url = url.replace("+", "%2B")
        typr = request.query_params.get('origin', "normal")
        if url.endswith('.m3u8'):
            if typr == "9anime":
                url += "#.mp4"
            async with session.get(url) as resp:
                headers = resp.headers.copy()
#                 ret_head = resp.headers.copy()
                ret_head = {}
                headers['Access-Control-Allow-Origin'] = '*'
                headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
                headers['Content-Disposition'] = 'attachment; filename="master.m3u8"'
                del_keys = ['Vary', 'Server', 'Report-To', 'NEL', 'Content-Encoding', 'Transfer-Encoding',
                            'Content-Length']
                del_ret = ['Content-Type', 'Content-Encoding', 'Transfer-Encoding', 'Content-Length', 'Access-Control-Allow-Origin', 'Report-To', 'Server',
                          'Access-Control-Allow-Methods', 'Access-Control-Allow-Credentials']
                for head in del_keys:
                    try:
                        del headers[head]
                    except KeyError:
                        pass
                for head in del_ret:
                    try:
                        del ret_head[head]
                    except KeyError:
                        pass
                text = await resp.text()
                base_url = '/'.join(url.split('/')[:-1]) + '/'
                modified_text = ''
                if ("404 not" not in text) and ("404 Not" not in text):
                    for line in text.split('\n'):
                        if line.startswith('#'):
                            modified_text += line + '\n'
                            continue
                        if line.startswith("https://"):
                            modified_text += '/cors?url=' + line + '&headers=' + json.dumps(
                                dict(ret_head)) + '\n'
                            continue
                        if not line.strip(" "):
                            continue
                        line = line.replace("+", "%2B")
                        modified_text += '/cors?url=' + base_url + line + "\n" # + '&headers=' + json.dumps(
                            # dict(ret_head)) + '\n'
                else:
                    modified_text = text
                return Response(content=modified_text, headers=headers)
        else:
            async with session.get(url) as resp:
                headers = resp.headers.copy()
                headers['Access-Control-Allow-Origin'] = '*'
                del_head = ['Vary', 'Server', 'Report-To', 'NEL', 'Transfer-Encoding', 'Content-Encoding', 'Content-Length']
                for key in del_head:
                    try:
                        del headers[key]
                    except KeyError:
                        pass
                data = await resp.read()
            return Response(content=data, headers=headers)


app.add_api_route('/cors', handle, methods=['GET'])
app.add_api_route('/', home, methods=['GET'])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5010)
