import requests
from django.conf import settings
from requests.exceptions import JSONDecodeError


def get_ip_info(ip_address: str) -> dict:
    """Return IP data as a dict using the IP Stack API."""
    params = {
        "fields": "main",
        "hostname": 1,
        "access_key": settings.IPSTACK_ACCESS_KEY,
    }
    r = requests.get(
        f"https://api.ipstack.com/{ip_address}",
        params=params,
        timeout=5,
    )
    r.raise_for_status()
    # IP Stack has been known to return 200, but not have JSON data
    try:
        return r.json()
    except JSONDecodeError:
        return {}
