import json
import aiohttp
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
    headers_['sec-ch-ua-platform'] = "\"Windows\""
    headers_['Sec-Fetch-Site'] = "same-site"
    headers_['Sec-Fetch-Mode'] = "cors"
    headers_['Sec-Fetch-Dest'] = "empty"
    headers_['Accept'] = "*/*"
    headers_['sec-ch-ua-mobile'] = "?0"
    async with aiohttp.ClientSession(headers=headers_) as session:
        url = request.query_params.get('url')
        if url.endswith('.m3u8'):
            async with session.get(url) as resp:
                headers = resp.headers.copy()
                ret_head = resp.headers.copy()
                headers['Access-Control-Allow-Origin'] = '*'
                headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
                headers['Content-Disposition'] = 'attachment; filename="master.m3u8"'
                del_keys = ['Vary', 'Server', 'Report-To', 'NEL', 'Content-Encoding', 'Transfer-Encoding',
                            'Content-Length']
                del_ret = ['Content-Type', 'Content-Encoding', 'Transfer-Encoding', 'Content-Length']
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
                for line in text.split('\n'):
                    if line.startswith('#'):
                        modified_text += line + '\n'
                        continue
                    if line.startswith("https://"):
                        modified_text += '/cors?url=' + line + '&headers=' + json.dumps(
                            dict(ret_head)) + '\n'
                        continue
                    modified_text += '/cors?url=' + base_url + line + '&headers=' + json.dumps(
                        dict(ret_head)) + '\n'
                return Response(content=modified_text, headers=headers)
        else:
            async with session.get(url) as resp:
                headers = resp.headers.copy()
                headers['Access-Control-Allow-Origin'] = '*'
                del_head = ['Vary', 'Server', 'Report-To', 'NEL', 'Transfer-Encoding', 'Content-Encoding']
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
