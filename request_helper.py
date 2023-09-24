from urllib.parse import urlparse, parse_qs, quote, unquote
import requests


class Requester:
    def __init__(self, url):
        parsed_url = urlparse(url)
        self.url = url
        self.schema = parsed_url.scheme
        self.domain = parsed_url.netloc
        self.query_params = self.query(parsed_url)
        self.host = self.get_host(parsed_url)
        self.path = parsed_url.path
        self.req_url = self.host + self.path
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/114.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                      'image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Referer': None,
            "SEC-CH-UA-MOBILE": "?0",
            "SEC-CH-UA-PLATFORM": "Linux",
        }

    def full(self, path_qs):
        return self.host + path_qs

    def get(self, data=None, headers=None, method='get', json_data=None, additional_params=None, cookies=None):
        headers = self.headers(headers)
        additional_params = {} if additional_params is None or type(additional_params) != dict else additional_params
        cookies = cookies if cookies else {}
        json_data = {} if json_data is None else json_data
        params = self.query_params.copy()
        params.update(additional_params)
        if method == "post":
            data = requests.post(self.req_url, headers=headers, params=params, data=data, timeout=35,
                                 json=json_data, allow_redirects=False, cookies=cookies)
        else:
            data = requests.get(self.req_url, headers=headers, params=params, data=data, timeout=35,
                                json=json_data, allow_redirects=False, cookies=cookies)
        return [data.content, data.headers, data.status_code, data.cookies]

    def headers(self, headers):
        header = self.base_headers.copy()
        header.update(headers if headers is not None else header)
        return header

    def safe(self, url):
        url = urlparse(url)
        queries = self.query(url)
        host = self.get_host(url)
        path = url.path
        return host + path + ("?" + self.query_string(queries) if queries else "")

    @staticmethod
    def safe_sub(url):
        return quote(url)

    @staticmethod
    def query(parsed_url):
        return {k: unquote(str(v[0]), 'utf-8') for k, v in dict(parse_qs(parsed_url.query)).items()}

    @staticmethod
    def query_string(queries: dict):
        strings = []
        for query in queries:
            strings.append(query + "=" + quote(queries[query]))
        return "&".join(strings)

    @staticmethod
    def get_host(parsed_url):
        host = parsed_url.scheme + '://' + parsed_url.netloc
        return host

    @staticmethod
    def m3u8(content):
        """
        it has been implemented in th cors.py file
        may be moved here in the future (not sure)
        :param content:
        :return:
        """
        pass

    def __str__(self):
        return f'Domain: {self.domain}\nScheme: {self.schema}\nPath: {self.path}\nquery parameters: {self.query_params}'

    @staticmethod
    def _cf_c(pgd):
        if "_cf_chl_opt" in pgd and "":
            pass


if __name__ == "__main__":
    _url = "https://example.com/test.mp4?token=3892&idea=2(]/s[e3r2&url=https%3A//example.com/test.mp4%3Ftoken%3D3892%26idea%3D2%28%5D/s%5Be3r2"
    er = Requester(_url)
    print(er)
