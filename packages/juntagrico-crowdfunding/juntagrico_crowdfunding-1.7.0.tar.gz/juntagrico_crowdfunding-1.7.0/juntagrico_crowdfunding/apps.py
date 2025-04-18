from django.apps import AppConfig


class JuntagricoCrowdfundingAppconfig(AppConfig):
    name = "juntagrico_crowdfunding"
    default_auto_field = 'django.db.models.AutoField'

    def ready(self):
        from juntagrico.util import addons
        addons.config.register_version(self.name)
