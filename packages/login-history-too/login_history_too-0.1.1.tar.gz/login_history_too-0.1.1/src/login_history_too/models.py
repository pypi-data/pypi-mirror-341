from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .mixins import IPAddressMixin
from .mixins import UserAgentMixin

User = get_user_model()


class UserLogin(UserAgentMixin, IPAddressMixin, models.Model):
    """Model to store user login history."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    ip_data = models.JSONField(null=True, blank=True)
    ua_data = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        tz = timezone.get_current_timezone()
        dt = self.timestamp.astimezone(tz)
        return f"{dt.strftime('%a %b %d, %Y at %-I:%M:%S %p')} from {self.ip_address}"
