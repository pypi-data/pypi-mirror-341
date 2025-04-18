# encoding: utf-8

from django.conf import settings
from juntagrico.config import Config


class CrowdfundingConfig:
    def __init__(self):
        pass

    @staticmethod
    def vocabulary(key):
        try:
            return Config.vocabulary(key)
        except KeyError:
            return {
                'funding_project': 'Unterstützungs-Projekt',
                'funding_project_pl': 'Unterstützungs-Projekte'
            }[key]

    @staticmethod
    def emails(key):
        if hasattr(settings, 'EMAILS'):
            if key in settings.EMAILS:
                return settings.EMAILS[key]
        return {'fund_confirmation_mail': 'cf/mails/fund_confirmation_mail.txt',
                }[key]
