from django.apps import AppConfig


class LoginHistoryTooConfig(AppConfig):
    name = "login_history_too"
    verbose_name = "Login History Too"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        import login_history_too.signals  # noqa: F401
