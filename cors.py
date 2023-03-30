# import json
#
# from aiohttp import web
# import aiohttp
#
#
# async def handle(request):
#     headers_ = request.query.get('headers',
#                                  "{\"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36}\"}")
#     headers_ = json.loads(headers_)
#     async with aiohttp.ClientSession(headers=headers_) as session:
#         url = request.query.get('url')
#         if url.endswith('.m3u8'):
#             async with session.get(url) as resp:
#                 headers = resp.headers.copy()
#                 ret_head = resp.headers.copy()
#                 headers['Access-Control-Allow-Origin'] = '*'
#                 headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
#                 headers['Content-Disposition'] = 'attachment; filename="master.m3u8"'
#                 del headers['Vary'], headers['Server'], headers['Report-To'], \
#                     headers['NEL'], headers['Content-Encoding']
#                 del ret_head["Content-Type"], ret_head["Content-Encoding"]
#                 try:
#                     del ret_head["Transfer-Encoding"], headers['Transfer-Encoding']
#                 except KeyError:
#                     pass
#                 text = await resp.text()
#                 base_url = '/'.join(url.split('/')[:-1]) + '/'
#                 modified_text = ''
#                 for line in text.split('\n'):
#                     if line.startswith('#'):
#                         modified_text += line + '\n'
#                         continue
#                     modified_text += '/cors?url=' + base_url + line + '&headers=' + json.dumps(
#                         dict(ret_head)) + '\n'
#                 return web.Response(text=modified_text, headers=headers)
#         else:
#             async with session.get(url) as resp:
#                 headers = resp.headers.copy()
#                 headers['Access-Control-Allow-Origin'] = '*'
#                 del headers['Vary'], headers['Server'], headers['Report-To'], \
#                     headers['NEL']
#                 try:
#                     del headers['Transfer-Encoding'], headers['Content-Encoding']
#                 except KeyError:
#                     pass
#                 data = (await resp.read())
#             return web.Response(body=data, headers=headers)
#
#
# app = web.Application()
# app.add_routes([web.get('/cors', handle)])
#
# if __name__ == '__main__':
#     web.run_app(app, port=5010)


# import json
# import aiohttp
# import shelve
# import time
# from aiohttp import web
# import asyncio
#
# CACHE_FILENAME = 'cache'
# CACHE_EXPIRATION_TIME = 3 * 60 * 60
#
#
# async def handle(request):
#     headers_ = request.query.get('headers',
#                                  "{\"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36}\"}")
#     try:
#         headers_ = json.loads(headers_)
#     except json.decoder.JSONDecodeError:
#         input(headers_)
#     async with aiohttp.ClientSession(headers=headers_) as session:
#         url = request.query.get('url')
#         with shelve.open(CACHE_FILENAME) as cache:
#             if url in cache:
#                 timestamp, response = cache[url]
#                 if (time.time() - timestamp) < CACHE_EXPIRATION_TIME:
#                     # pass
#                     return response
#                 else:
#                     del cache[url]
#             if url.endswith('.m3u8'):
#                 async with session.get(url) as resp:
#                     headers = resp.headers.copy()
#                     ret_head = resp.headers.copy()
#                     headers['Access-Control-Allow-Origin'] = '*'
#                     headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
#                     headers['Content-Disposition'] = 'attachment; filename="master.m3u8"'
#                     del_keys = ['Vary', 'Server', 'Report-To', 'NEL', 'Content-Encoding', 'Transfer-Encoding', 'Content-Length']
#                     del_ret = ['Content-Type', 'Content-Encoding', 'Transfer-Encoding', 'Content-Length']
#                     for key in del_keys:
#                         try:
#                             del headers[key]
#                         except KeyError:
#                             pass
#                     for key in del_ret:
#                         try:
#                             del ret_head[key]
#                         except KeyError:
#                             pass
#                     text = await resp.text()
#                     base_url = '/'.join(url.split('/')[:-1]) + '/'
#                     modified_text = ''
#                     ret_head = dict(ret_head)
#                     dump_ret = json.dumps(ret_head)
#                     for line in text.split('\n'):
#                         if line.startswith('#'):
#                             modified_text += line + '\n'
#                             continue
#                         modified_text += '/cors?url=' + base_url + line + '&headers=' + dump_ret + '\n'
#                     response = web.Response(body=modified_text, headers=headers)
#             else:
#                 async with session.get(url) as resp:
#                     headers = resp.headers.copy()
#                     headers['Access-Control-Allow-Origin'] = '*'
#                     del_head = ['Vary', 'Server', 'Report-To', 'NEL', 'Transfer-Encoding', 'Content-Encoding']
#                     for key in del_head:
#                         try:
#                             del headers[key]
#                         except KeyError:
#                             pass
#                     data = await resp.read()
#                     response = web.Response(body=data, headers=headers)
#             cache[url] = [time.time(), response]
#             print('new fetch')
#             return response
#
#
# async def cache_cleanup():
#     while True:
#         with shelve.open(CACHE_FILENAME) as cache:
#             for url, data in cache.items():
#                 cached_time = data['timestamp']
#                 current_time = time.time()
#                 if current_time - cached_time > CACHE_EXPIRATION_TIME:
#                     del cache[url]
#         await asyncio.sleep(10 * 60)
#
#
# app = web.Application()
# app.add_routes([web.get('/cors', handle)])
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.create_task(cache_cleanup())
#     web.run_app(app, port=5010)


import json
import os
import secrets
import time
import asyncio
import aioredis
import aiohttp
from aiohttp import web
import redis

CACHE_EXPIRATION_TIME = 3 * 60 * 60


async def handle(request):
    headers_ = request.query.get('headers',
                                 "{\"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36}\"}")
    try:
        headers_ = json.loads(headers_)
    except json.decoder.JSONDecodeError:
        input(headers_)
    async with aiohttp.ClientSession(headers=headers_) as session:
        url = request.query.get('url')
        redis_ = request.app['redis']
        cached_response = await redis_.get(url)
        if cached_response is not None:
            cached_response = json.loads(cached_response)
            if (time.time() - cached_response['timestamp']) < CACHE_EXPIRATION_TIME:
                response_headers = cached_response['headers']
                response_body = cached_response['body']
                response_body = open(response_body, 'rb').read()
                return web.Response(body=response_body, headers=response_headers)
        print(url)
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
                for key in del_keys:
                    try:
                        del headers[key]
                    except KeyError:
                        pass
                for key in del_ret:
                    try:
                        del ret_head[key]
                    except KeyError:
                        pass
                text = await resp.text()
                base_url = '/'.join(url.split('/')[:-1]) + '/'
                modified_text = ''
                ret_head = dict(ret_head)
                dump_ret = json.dumps(ret_head)
                for line in text.split('\n'):
                    if line.startswith('#'):
                        modified_text += line + '\n'
                        continue
                    modified_text += '/cors?url=' + base_url + line + '&headers=' + dump_ret + '\n'
                response = web.Response(body=modified_text, headers=headers)
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
                response = web.Response(body=data, headers=headers)
            response_headers = dict(response.headers)
            # data_file = url.replace('/', '_')
            name = ""
            charset = "abcdefghijklmonpqrstuvwxyzABCDEFGHIJKLMNOPQRSTUBWXYZ0123456789"
            for i in range(50):
                name += secrets.choice(charset)
            data_file = name + url.split('.')[-1]
            with open(data_file, 'wb') as f_cache:
                f_cache.write(data)
            cached_response = {
                'timestamp': time.time(),
                'headers': response_headers,
                'body': data_file,
            }
            await redis_.set(url, json.dumps(cached_response))
        return response


async def cache_cleanup(app):
    while True:
        redis_ = app['redis']
        keys = await redis_.keys('*')
        for key in keys:
            cached_response = await redis_.get(key)
            if cached_response is not None:
                cached_response = json.loads(cached_response)
                if (time.time() - cached_response['timestamp']) < CACHE_EXPIRATION_TIME:
                    cached_response.delete(key)
                    os.remove(cached_response['body'])
        await asyncio.sleep(10 * 60)


async def create_redis_pool():
    redis_pool = await aioredis.Redis.from_url('redis://localhost')
    return redis_pool


r = redis.Redis(host='localhost', port=6379)
r.set('mykey', 'myvalue')
value = r.get('mykey')
print(value)

loop = asyncio.get_event_loop()
redis_instance = asyncio.run(create_redis_pool())
app = web.Application()
app['redis'] = redis_instance
app.add_routes([web.get('/cors', handle)])
if __name__ == '__main__':
    loop.create_task(cache_cleanup(app))
    web.run_app(app, port=5010)
