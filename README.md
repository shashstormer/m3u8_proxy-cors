# m3u8_proxy-cors

This is a simple Python proxy server that adds CORS headers to M3U8 playlist files. It allows you to bypass CORS restrictions when playing M3U8 playlists in browsers.

## Installation

To install and run the server, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/shashstormer/m3u8_proxy-cors.git
    ```
2. Install dependencies:
    
    ```bash
    cd m3u8_proxy-cors
    pip install -r requirements.txt
    ```
3. Start the server:
    ```bash
    python main.py
    ```

The server will start listening on port 5010 by default. You can change the port by setting the `port` environment variable

You may configure which domains can use this proxy by setting the `origins` environment variable, by default it will allow all origins for people who wish to use it just as the older version

You may enable or disable the documentation which is available on the /docs path by setting `documentation` as 
- `True` to enable
- `False` to disable (**Default**)

you may also change the documentation url by setting the `docs_url` and `redoc_url` environment variable, default value is '**_/docs_**' and '**_/redoc_**' by default
- setting the value as '' _(empty string)_ will remove the documentation (useful in cases when you want only one documentation)
- **Setting the documentation env variable as False will remove both the documentation and these env variables will have no effect** 
- `docs_url` is for _swagger documentation_ and `redoc_url` is for _redoc documentation_


## Usage

To use the server, simply replace the URL of the M3U8 playlist file in your application with the URL of the proxy server. For example, if your original URL was `https://example.com/video.m3u8`, you would replace it with `http://localhost:5010/cors?url=https://example.com/video.m3u8`.

To set custom headers for a request you can do ```http://localhost:5010/cors?url=https://example.com/video.m3u8&headers={"User-Agent":"Mozilla/5.0 ...","referer":"https://example.com",...}```

don't put spaces between the headers (you can put it inside the quotes) you might get a 500 error,

## Deploying to Vercel
You can quickly deploy this project to Vercel with the following button:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fshashstormer%2Fm3u8_proxy-cors&project-name=m3u8-proxy-cors&repository-name=m3u8-proxy-cors)

## Security issues

1. > coppies user cookies while requesting. This leads to possibility of leakage of acces tokens. vulnerability will be fixed in future
use older version to bypass vulnerability
if you wish to use latest features you may host this on a different domain than your site.

contributions are welcome you can make a pull request I will review it and merge it if it benifits the program
