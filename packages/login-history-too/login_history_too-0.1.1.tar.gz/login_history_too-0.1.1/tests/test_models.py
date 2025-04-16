import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from login_history_too.models import UserLogin

User = get_user_model()

pytestmark = pytest.mark.django_db


def test___str__():
    user = User.objects.create_user(username="testuser", password="testpassword")
    # Create a test instance
    obj = UserLogin.objects.create(
        user=user, timestamp=timezone.now(), ip_address="192.168.1.1"
    )

    # Get the current timezone
    tz = timezone.get_current_timezone()

    # Format the timestamp according to the expected format
    expected_timestamp = obj.timestamp.astimezone(tz).strftime(
        "%a %b %d, %Y at %-I:%M:%S %p"
    )

    # Check if the __str__ method returns the expected string
    assert str(obj) == f"{expected_timestamp} from {obj.ip_address}"
