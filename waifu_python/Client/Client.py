import httpx
from httpx_socks import AsyncProxyTransport

Connection = httpx.Limits(max_keepalive_connections=20, max_connections=100)

transport = AsyncProxyTransport.from_url("http://43.135.130.198:13001")

client = httpx.AsyncClient(
    transport=transport,
    timeout=15.0,
    follow_redirects=True,
    limits=Connection,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 15.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"
    }
)

DEFAULT_HEADERS = {
    "User-Agent": "WaifuPython/1.0 akoushik88@gmail.com"
}