# -*- coding: utf-8  -*-

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from .models import SACYear, Position, Nomination, NominationAnnouncement, VoteNomination, city_choices
from .forms import NominationForm
from . import decorators, utils
from django.db.models import Count


def show_index(request):
    if request.user.is_authenticated():
        return render(request, 'accounts/home.html')
    else:
        return render(request, 'accounts/home_unauthenticated.html')

@login_required
def list_positions(request, entity):
    current_year = SACYear.objects.get_current()
    if not current_year.is_nomination_open():
        return HttpResponseRedirect(reverse("voting:closed"))

    if entity in ['club', 'council']:
        user_nominations = Nomination.objects.filter(position__entity=entity,
                                                     user=request.user)
        positions = Position.objects.filter(entity=entity)
        if not request.user.is_superuser:
            positions = positions.filter(colleges_allowed_to_nominate=request.user.profile.college)
    else:
        raise Http404

    context = {'user_nominations': user_nominations,
               'positions': positions}
    return render(request, 'voting/list_' + entity + '_positions.html', context)

@login_required
def add_nominee(request, position_id):
    current_year = SACYear.objects.get_current()
    if not current_year.is_nomination_open():
        return HttpResponseRedirect(reverse("voting:closed"))

    position = get_object_or_404(Position, pk=position_id)
    context = {'position': position}

    user_nominations = Nomination.objects.filter(position__entity=position.entity,
                                                 user=request.user)
    if user_nominations.exists():
        context['already_on'] = True
    else:
        if request.user.is_superuser:
            positions = Position.objects.all()
        else:
            positions = Position.objects.filter(colleges_allowed_to_nominate=request.user.profile.college)
            if position not in positions:
                raise PermissionDenied
        if request.method == 'POST':
            instance = Nomination(user=request.user, position=position)
            form = NominationForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                instance = form.save()
                print instance.pk
                return HttpResponseRedirect(reverse("voting:nomination_thanks", args=(position.pk,)))
        elif request.method == 'GET':
            form = NominationForm()
        context['form'] = form

    return render(request,'voting/add_nominee.html', context)

@login_required
def show_nomination(request, position_id, nomination_id):
    nomination = get_object_or_404(Nomination, position__pk=position_id,
                                 pk=nomination_id)
    if not request.user.is_superuser and \
       not nomination.user == request.user:
        raise PermissionDenied
    context = {'nomination': nomination}
    return render(request,'voting/show_nomination.html', context)

def announce_nominees(request, entity):
    current_year = SACYear.objects.get_current()
    context = {}
    if current_year.is_announcement_due():
        if entity in ['club', 'council']:
            per_city = []
            for city_code, city_name in city_choices:
                position = Position.objects\
                                   .filter(entity=entity, city=city_code)\
                                   .annotate(nomination_count=Count('nominationannouncement'))\
                                   .filter(nomination_count__gt=1)
                per_city.append((city_name, position))
            context = {'entity': entity, 'per_city': per_city}
            
        else:
            raise Http404

    return render(request, 'voting/announce_nominees.html', context)

@login_required
def show_voting_index(request):
    current_year = SACYear.objects.get_current()
    if not current_year.is_voting_open():
        return HttpResponseRedirect(reverse("voting:voting_closed"))
    else:
        qrcode_value = utils.get_ticket(request.user)
        context = {'qrcode_value': qrcode_value}
        return render(request,'voting/show_voting.html', context)

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def handle_vote(request):
    current_year = SACYear.objects.get_current()
    if not current_year.is_voting_open():
        return HttpResponseRedirect(reverse("voting:voting_closed"))
    else:
        nomination_vote_pk = request.POST.get('nomination_vote_pk', None)
        if nomination_vote_pk:
            nomination_announcement = NominationAnnouncement.objects.get(pk=nomination_vote_pk)
            previous_vote = VoteNomination.objects.filter(nomination_announcement=nomination_announcement,
                                                          user=request.user).exists()
            if not request.user.is_superuser and \
                request.user.profile.college not in\
                    nomination_announcement.position.colleges_allowed_to_vote:
                raise PermissionDenied
            else:
                if previous_vote:
                    raise Exception('سبق أن صوتّ لهذا المنصب')
                else:
                    VoteNomination.objects.create(nomination_announcement=nomination_announcement,
                                                  user=request.user)

        position_pool = Position.objects.annotate(announced_count=Count('nominationannouncement'))\
                                        .filter(announced_count__gte=2)\
                                        .exclude(nominationannouncement__votenomination__user=request.user)
        if request.user.is_superuser:
            next_position = position_pool.first()
        else:
            next_position = position_pool.filter(colleges_allowed_to_vote=request.user.profile.college)\
                                         .first()
        if next_position:
            nominations = []
            for nomination in next_position.nominationannouncement_set.all():
                nomination = {'pk': nomination.pk,
                              'nominee_name': nomination.user.username,
                              'plan': nomination.plan.url,
                              'cv': nomination.cv.url}
                nominations.append(nomination)
            return {"position_title": next_position.title,
                    "nominations": nominations}
        else:
            qrcode_value = utils.get_ticket(request.user)
            votes = VoteNomination.objects.filter(user=request.user,
                                                  nomination_announcement__position__year=
                                                  current_year)
            return {'done': 1, 'qrcode_value': qrcode_value, 'votes': votes}



def get_stats(request):
    return HttpResponseRedirect(reverse("voting:stats"))