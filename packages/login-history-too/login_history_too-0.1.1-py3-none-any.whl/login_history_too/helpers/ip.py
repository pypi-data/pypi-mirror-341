import functools
import ipaddress
import logging

from django.conf import settings

from login_history_too.settings import api_settings

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1024)
def get_ip_info(ip_address) -> dict:
    """
    Wrapper function to get IP data from the configured API. Ignores internal
    and private IP addresses.
    """
    if ip_address in settings.INTERNAL_IPS or is_private_ip(ip_address):
        logger.warning("IP address is internal or private: %s", ip_address)
        return {}

    try:
        return api_settings.GEOLOCATION_METHOD(ip_address)
    except Exception as e:  # noqa: BLE001
        logger.warning("Could not get IP info from API: %s", str(e))
        return {}


def is_private_ip(ip_address: str) -> bool:
    """
    This function checks if the given IP address is private.

    Args:
        ip_address (str): The IP address to check.

    Returns:
        bool: True if the IP address is private, False otherwise.
    """
    try:
        return ipaddress.ip_address(ip_address).is_private
    except ValueError:
        logger.warning("Invalid IP address: %s", ip_address)
        return False
