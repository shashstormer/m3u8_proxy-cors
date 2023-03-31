# m3u8_proxy-cors

This is a simple Python proxy server that adds CORS headers to M3U8 playlist files. It allows you to bypass CORS restrictions when playing M3U8 playlists in browsers.

## Installation

To install and run the server, follow these steps:

1. Clone the repository:

```py
git clone https://github.com/LiReNa00/m3u8_proxy-cors.git
```

2. Install dependencies:
    
```py
cd m3u8_proxy-cors
pip install -r requirements.txt
```
3. Start the server:
```py
python main.py
```

The server will start listening on port 5010 by default. You can change the port by setting the `port` variable in main.py

## Usage

To use the server, simply replace the URL of the M3U8 playlist file in your application with the URL of the proxy server. For example, if your original URL was `http://example.com/video.m3u8`, you would replace it with `http://localhost:5010/cors?urlhttp://example.com/video.m3u8`.

## Deploying to Vercel
You can quickly deploy this project to Vercel with the following button:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmasterz5398%2Fm3u8_proxy-cors&project-name=m3u8-proxy-cors&repository-name=m3u8-proxy-cors)
