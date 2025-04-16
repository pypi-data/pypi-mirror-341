from login_history_too.helpers.ip import get_ip_info as get_ip_info_wrapper
from login_history_too.utils import get_ip_info


def test_get_ip_info():
    ip_address = "8.8.8.8"
    result = get_ip_info(ip_address)
    assert isinstance(result, dict)
    assert "ip" in result


def test_get_ip_info_internal_ip():
    ip_address = "192.168.1.1"
    assert get_ip_info_wrapper(ip_address) == {}


def test_get_ip_info_private_ip():
    ip_address = "10.0.0.1"
    assert get_ip_info_wrapper(ip_address) == {}
