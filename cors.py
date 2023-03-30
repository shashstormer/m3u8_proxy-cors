import json

from aiohttp import web
import aiohttp


async def handle(request):
    headers_ = request.query.get('headers',
                                 "{\"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36}\"}")
    headers_ = json.loads(headers_)
    async with aiohttp.ClientSession(headers=headers_) as session:
        url = request.query.get('url')
        if url.endswith('.m3u8'):
            async with session.get(url) as resp:
                headers = resp.headers.copy()
                ret_head = resp.headers.copy()
                headers['Access-Control-Allow-Origin'] = '*'
                headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
                headers['Content-Disposition'] = 'attachment; filename="master.m3u8"'
                del headers['Vary'], headers['Server'], headers['Report-To'], \
                    headers['NEL'], headers['Content-Encoding']
                del ret_head["Content-Type"], ret_head["Content-Encoding"]
                try:
                    del ret_head["Transfer-Encoding"], headers['Transfer-Encoding']
                except KeyError:
                    pass
                text = await resp.text()
                base_url = '/'.join(url.split('/')[:-1]) + '/'
                print(text)
                # input(base_url)
                modified_text = ''
                for line in text.split('\n'):
                    if line.startswith('#'):
                        modified_text += line + '\n'
                        continue
                    modified_text += '/cors?url=' + base_url + line + '&headers=' + json.dumps(
                        dict(ret_head)) + '\n'
                return web.Response(text=modified_text, headers=headers)
        else:
            async with session.get(url) as resp:
                headers = resp.headers.copy()
                headers['Access-Control-Allow-Origin'] = '*'
                del headers['Vary'], headers['Server'], headers['Report-To'], \
                    headers['NEL']
                try:
                    del headers['Transfer-Encoding'], headers['Content-Encoding']
                except KeyError:
                    pass
                data = (await resp.read())
            return web.Response(body=data, headers=headers)


app = web.Application()
app.add_routes([web.get('/cors', handle)])

if __name__ == '__main__':
    web.run_app(app, port=5010)
