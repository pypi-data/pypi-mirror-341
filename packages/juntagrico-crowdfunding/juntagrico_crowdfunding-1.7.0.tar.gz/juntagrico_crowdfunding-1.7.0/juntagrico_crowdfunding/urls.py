"""juntagrico_crowdfunding URL Configuration
"""
from django.urls import path
from juntagrico_crowdfunding import views as crowdfunding

app_name = 'jcf'
urlpatterns = [
    path(r'cf', crowdfunding.list_funding_projects, name='home'),
    path(r'cf/list/<int:funding_project_id>', crowdfunding.list_fundables, name='list'),
    path(r'cf/view/<int:fundable_id>', crowdfunding.view_fundable, name='view'),
    path(r'cf/fund/<int:fundable_id>', crowdfunding.fund, name='fund'),
    path(r'cf/confirm', crowdfunding.confirm, name='confirm'),
    path(r'cf/edit/order', crowdfunding.edit_order, name='edit-order'),
    path(r'cf/edit/funder', crowdfunding.edit_funder, name='edit-funder'),
    path(r'cf/thanks/<int:funding_project_id>', crowdfunding.thanks, name='thanks'),
    path(r'cf/contribution', crowdfunding.contribution, name='contribution'),
]
