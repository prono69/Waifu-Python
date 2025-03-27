
import httpx
from httpx_socks import AsyncProxyTransport

proxy_url = "http://43.135.130.198:13001"  
if proxy_url:
    transport = AsyncProxyTransport.from_url(proxy_url)
else:
    transport = None

Connection = httpx.Limits(max_keepalive_connections=20, max_connections=100)

DEFAULT_HEADERS = {
    "User-Agent": "WaifuPython/1.0 akoushik88@gmail.com"
}

if transport:
    print("proxy detected")
    client = httpx.AsyncClient(
        transport=transport,
        timeout=15.0,
        follow_redirects=True,
        limits=Connection,
        headers=DEFAULT_HEADERS
    )
else:
    client = httpx.AsyncClient(
        timeout=15.0,
        follow_redirects=True,
        limits=Connection,
        headers=DEFAULT_HEADERS
    )
