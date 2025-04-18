from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from juntagrico_crowdfunding.entity.fund import Fund
from juntagrico_crowdfunding.entity.fundable import Fundable
from juntagrico_crowdfunding.entity.funder import Funder
from juntagrico_crowdfunding.entity.funding_project import FundingProject

from juntagrico.util.management import password_generator

from juntagrico_crowdfunding.forms import FundForm, RegisterFunderForm
from juntagrico_crowdfunding.mailer import send_fund_confirmation_mail

from juntagrico.view_decorators import highlighted_menu


def lost_session(request):
    """
    Session lost. start over
    """
    return render(request, "cf/session_lost.html")


@highlighted_menu('crowdfunding')
def list_funding_projects(request):
    """
    List of fundingprojects
    """

    funding_projects = FundingProject.objects.filter(active=True)
    # don't show selection if only one active funding project exists
    if funding_projects.count() == 1:
        return list_fundables(request, funding_projects[0].id)

    else:
        renderdict = {
            'funding_projects': funding_projects
        }
        return render(request, "cf/list_funding_projects.html", renderdict)


@highlighted_menu('crowdfunding')
def list_fundables(request, funding_project_id):
    """
    List of fundables
    """

    fundables = Fundable.objects.filter(funding_project_id=funding_project_id)

    my_funds = False
    if request.user.is_authenticated:  # logged in
        if hasattr(request.user, 'funder'):  # is funder
            my_funds = Fund.objects.filter(funder=request.user.funder, fundable__funding_project=funding_project_id)

    renderdict = {
        'fp': FundingProject.objects.filter(id=funding_project_id)[0],
        'fundables': fundables,
        'my_funds': my_funds
    }

    return render(request, "cf/list_fundables.html", renderdict)


@highlighted_menu('crowdfunding')
def view_fundable(request, fundable_id):
    """
    Details of fundable
    """

    fundable = Fundable.objects.filter(id=fundable_id)[0]

    # evaluate form
    if request.method == 'POST':
        # store order
        fund_form = FundForm(fundable.available, request.POST)
    elif request.session.get('pastorder') is not None:  # when changing order
        fund_form = FundForm(fundable.available, request.session.get('pastorder'))
    else:
        fund_form = FundForm(fundable.available)

    fund_form.fields['fundable'].initial = fundable  # set fundable in form
    if hasattr(request.user, "funder"):
        fund_form.fields['sponsor'].initial = request.user.funder.first_name  # set fundable in form

    if request.method == 'POST':
        if fund_form.is_valid():
            request.session['order'] = fund_form.cleaned_data
            request.session['pastorder'] = None  # clear
            return HttpResponseRedirect(reverse('jcf:confirm'))

    renderdict = {
        'fundable': fundable,
        'public_funds': fundable.fund_set.all,
        'fundForm': fund_form
    }
    return render(request, "cf/view_fundable.html", renderdict)


@highlighted_menu('crowdfunding')
def fund(request, fundable_id):
    """
    Confirm funding
    """

    fundable = Fundable.objects.filter(id=fundable_id)[0]

    renderdict = {
        'fundable': fundable
    }
    return render(request, "cf/fund.html", renderdict)


@highlighted_menu('crowdfunding')
def signup(request):
    initial = {}
    if hasattr(request.user, 'member'):  # copy from juntagrico member if available
        member = request.user.member
        initial = {
            'first_name': member.first_name,
            'last_name': member.last_name,
            'addr_street': member.addr_street,
            'addr_zipcode': member.addr_zipcode,
            'addr_location': member.addr_location,
            'phone': member.phone,
            'email': member.email
        }

    if request.method == 'POST':
        funder_form = RegisterFunderForm(request.POST, initial=initial)
    elif request.session.get('pastfunder') is not None:  # when changing funder
        funder_form = RegisterFunderForm(instance=request.session.get('pastfunder'))
    else:
        funder_form = RegisterFunderForm(initial=initial)

    renderdict = {
        'funderform': funder_form
    }
    return render(request, "cf/signup.html", renderdict)


@highlighted_menu('crowdfunding')
def confirm(request):
    """
    Confirm Fund
    """

    funder = False

    # 1. form evaluation
    if request.method == 'POST':
        # create funder from form
        funderform = RegisterFunderForm(request.POST)
        # TODO: Wenn E-mail schon existiert, darauf hinweisen, dass Benutzer sich einloggen soll.
        if funderform.is_valid():
            print("creating funder")
            funder = Funder(**funderform.cleaned_data)
            request.session['funder'] = funder

    # get funder (existing or about to be created)
    if request.user.is_authenticated and hasattr(request.user, 'funder'):
        # existing funder
        funder = request.user.funder
    elif request.session.get('funder') is not None:
        # new funder
        funder = request.session['funder']

    # if no user is logged in: show form to login or register
    if not funder:
        return signup(request)

    # process order
    order = request.session.get('order')
    if order is None:
        return lost_session(request)  # session expired
    else:
        order.update({'contribution': order.get('quantity') * order.get('fundable').price})

    # save confirmed order
    if request.POST.get('confirm') == '1':
        password = None
        if request.user.is_authenticated:
            funder.user = request.user
        else:
            password = password_generator()
            funder.user = User.objects.create_user(username=funder.email, password=password)

        fund = Fund(
            funder=funder,
            contribution=order.get('contribution'),
            fundable=order.get('fundable'),
            sponsor=order.get('sponsor'),
            message=order.get('message')
        )
        funding_project_id = order.get('fundable').funding_project.id

        # send confirmation email
        send_fund_confirmation_mail(fund, password)

        funder.user.save()
        funder.save()
        fund.funder = funder
        fund.save()

        # clear session and show thanks message
        request.session['funder'] = None
        request.session['pastfunder'] = None
        request.session['order'] = None
        request.session['pastorder'] = None
        return HttpResponseRedirect(reverse('jcf:thanks', args=[funding_project_id]))

    # show summary to confirm
    renderdict = {
        'order': order,
        'funder': funder
    }
    return render(request, "cf/confirm.html", renderdict)


@highlighted_menu('crowdfunding')
def edit_order(request):
    """
    go back to order page
    """

    if not request.session.get('order'):
        return lost_session(request)  # session expired

    # delete order from session and pass its content to the order form
    request.session['pastorder'] = request.session.get('order')
    request.session['order'] = None
    return HttpResponseRedirect(reverse('jcf:view', args=[request.session['pastorder'].get('fundable').id]))


@highlighted_menu('crowdfunding')
def edit_funder(request):
    """
    change funder but keep order
    """

    # logout in case funder is logged in
    if request.user.is_authenticated and hasattr(request.user, "funder"):
        order = request.session.get('order')  # keep order
        logout(request)
        request.session['order'] = order
    else:
        # clear funder
        request.session['pastfunder'] = request.session.get('funder')
        request.session['funder'] = None

    return HttpResponseRedirect(reverse('jcf:confirm'))


@highlighted_menu('crowdfunding')
def thanks(request, funding_project_id=None):
    """
    Thank you page
    """

    renderdict = {}
    if funding_project_id:
        renderdict.update({'funding_project': FundingProject.objects.get(id=funding_project_id)})
    return render(request, "cf/thanks.html")


@login_required
@highlighted_menu('crowdfunding')
def contribution(request):
    """
    List of personal contributions
    """

    contributions = False
    if hasattr(request.user, 'funder'):  # is funder
        contributions = Fund.objects.filter(funder=request.user.funder)

    renderdict = {
        'contributions': contributions
    }
    return render(request, "cf/contribution.html", renderdict)
