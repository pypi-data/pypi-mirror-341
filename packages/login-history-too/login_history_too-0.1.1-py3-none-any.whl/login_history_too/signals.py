from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from ipware import get_client_ip

from .helpers.ip import get_ip_info
from .helpers.ua import get_ua_info
from .models import UserLogin


@receiver(user_logged_in)
def track_user_login(sender, request, user, **kwargs):
    # Get user agent data
    ua_string = request.headers.get("user-agent")
    ua_data = get_ua_info(ua_string) if ua_string else {}

    # Get ip address data
    ip_address, _ = get_client_ip(request)
    ip_data = get_ip_info(ip_address) if ip_address else {}

    UserLogin.objects.create(
        user=user, ip_address=ip_address, ua_data=ua_data, ip_data=ip_data
    )
