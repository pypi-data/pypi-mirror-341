from django import template
from juntagrico_crowdfunding.config import CrowdfundingConfig
from juntagrico_crowdfunding.entity.funding_project import FundingProject

register = template.Library()


@register.simple_tag
def vocabulary(key):
    return CrowdfundingConfig.vocabulary(key)


@register.simple_tag
def has_active_funding_projects():
    return FundingProject.objects.filter(active=True).count() > 0
