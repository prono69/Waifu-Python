import os
import random
import httpx
from httpx_socks import AsyncProxyTransport
from httpx import Limits

DEFAULT_HEADERS = {
    "User-Agent": "WaifuPython/1.0 akoushik88@gmail.com"
}
Connection = Limits(max_keepalive_connections=200, max_connections=1000)

client = httpx.AsyncClient(
    timeout=15.0,
    follow_redirects=True,
    limits=Connection,
    headers=DEFAULT_HEADERS
)

def get_random_proxy() -> str:
    proxy_api_url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"
    try:
        response = httpx.get(proxy_api_url, timeout=10)
        response.raise_for_status()
        proxies = response.text.strip().splitlines()
        if proxies:
            top_proxies = proxies[:10]
            selected = random.choice(top_proxies)
            print(f"Selected proxy: {selected}")
            return selected
    except Exception as e:
        print(f"Error fetching proxies: {e}")
    return ""

def get_dynamic_client(use_proxy: bool = False) -> httpx.AsyncClient:

    if use_proxy:
        proxy_url = get_random_proxy()
        if proxy_url:
            transport = AsyncProxyTransport.from_url(proxy_url)
            return httpx.AsyncClient(
                transport=transport,
                timeout=15.0,
                follow_redirects=True,
                limits=Connection,
                headers=DEFAULT_HEADERS
            )

    return client