from django.template.loader import get_template

from juntagrico.config import Config
from juntagrico.mailer import EmailSender, base_dict

from juntagrico_crowdfunding.config import CrowdfundingConfig

'''
Server generated Emails
'''


def send_fund_confirmation_mail(fund, password=None):
    plaintext = get_template(CrowdfundingConfig.emails('fund_confirmation_mail'))
    content = plaintext.render(base_dict(locals()))
    EmailSender.get_sender(
        Config.organisation_name() + ' - Beitragsbestätigung',
        content).send_to(fund.funder.email)
