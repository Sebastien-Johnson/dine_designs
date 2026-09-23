from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    #loads signal
    def ready(self):
        import accounts.signals
