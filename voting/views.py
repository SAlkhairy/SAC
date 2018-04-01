# -*- coding: utf-8  -*-
from dal import autocomplete
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from .forms import NominationForm
from .models import SACYear, Position, Nomination, \
                    NominationAnnouncement, VoteNomination, \
                    city_choices
from . import decorators, utils
import accounts.utils
import re

def show_index(request):
    if request.user.is_authenticated():
        return render(request, 'accounts/home.html')
    else:
        return render(request, 'accounts/home_unauthenticated.html')

@login_required
def list_positions(request, entity):
    current_year = SACYear.objects.get_current()
    if not current_year.is_nomination_open():
        return render(request, "voting/closed.html")

    user_nominations = Nomination.objects.filter(position__entity=entity,
                                                 position__year=current_year,
                                                 user=request.user)
    positions = Position.objects.filter(entity=entity, year=current_year)
    if not request.user.is_superuser:
        positions = positions.filter(colleges_allowed_to_nominate=request.user.profile.college)

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
                                                 position__year=current_year,
                                                 user=request.user)
    if user_nominations.exists():
        context['already_on'] = True
    else:
        if request.user.is_superuser:
            positions = Position.objects.filter(year=current_year)
        else:
            positions = Position.objects.filter(colleges_allowed_to_nominate=request.user.profile.college,
                                                year=current_year)
            if position not in positions:
                raise PermissionDenied
        if request.method == 'POST':
            instance = Nomination(user=request.user, position=position)
            form = NominationForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                instance = form.save()
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
        per_city = []
        for city_code, city_name in city_choices:
            positions = Position.objects\
                               .filter(entity=entity, city=city_code, year=current_year)\
                               .annotate(nomination_count=Count('nominationannouncement'))\
                               .filter(nomination_count__gt=1)
            if positions.exists():
                per_city.append((city_name, positions))
        context = {'entity': entity, 'per_city': per_city}

    return render(request, 'voting/announce_nominees.html', context)

@login_required
def show_voting_index(request):
    current_year = SACYear.objects.get_current()
    if not request.user.is_superuser and not current_year.is_voting_open():
        return render(request, "voting/voting_closed.html")
    else:
        position_pool = Position.objects.annotate(announced_count=Count('nominationannouncement'))\
                                        .filter(announced_count__gte=2)\
                                        .exclude(votenomination__user=request.user)\
                                        .order_by('entity')
        if request.user.profile:
            position_pool = position_pool.filter(colleges_allowed_to_vote=request.user.profile.college)

        if position_pool.exists():
            completed_voting = False
            votes = VoteNomination.objects.none()
        else:
            completed_voting = True
            votes = VoteNomination.objects.filter(user=request.user)
        qrcode_value = utils.get_ticket(request.user)
        context = {'qrcode_value': qrcode_value,
                   'completed_voting': completed_voting,
                   'votes': votes}
        return render(request,'voting/show_voting.html', context)

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def handle_vote(request):
    current_year = SACYear.objects.get_current()
    if not request.user.is_superuser and not current_year.is_voting_open():
        raise Exception("التصويت غير مُتاح حاليًا!")

    nomination_vote_pk = request.POST.get('nomination_vote_pk', None)
    if nomination_vote_pk:
        if nomination_vote_pk == 'skip':
            position_pk = request.POST.get('position_pk')
            nomination_announcement = None
            position = Position.objects.get(pk=position_pk)
        else:
            nomination_announcement = NominationAnnouncement.objects.get(pk=nomination_vote_pk)
            position = nomination_announcement.position

        previous_vote = VoteNomination.objects.filter(position=position,
                                                      user=request.user).exists()
        if previous_vote:
            raise Exception(u'سبق أن صوتّ لهذا المنصب')

        if not request.user.is_superuser and \
           not request.user.profile.college in\
               nomination_announcement.position.colleges_allowed_to_vote.all():
            raise PermissionDenied
        else:
            VoteNomination.objects.create(nomination_announcement=nomination_announcement,
                                          position=position,
                                          user=request.user)

    position_pool = Position.objects.annotate(announced_count=Count('nominationannouncement'))\
                                    .filter(announced_count__gte=2)\
                                    .exclude(votenomination__user=request.user)
    if request.user.is_superuser:
        next_position = position_pool.first()
    else:
        next_position = position_pool.filter(colleges_allowed_to_vote=request.user.profile.college)\
                                     .first()
    if next_position:
        nominations = []
        for nomination in next_position.nominationannouncement_set.order_by('user__profile__ar_first_name'):
            nomination = {'pk': nomination.pk,
                          'nominee_name': nomination.user.profile.get_ar_full_name(),
                          'plan': nomination.plan.url,
                          'cv': nomination.cv.url}
            nominations.append(nomination)
        return {"position_title": next_position.title,
                "position_pk": next_position.pk,
                "entity": next_position.entity,
                "note": next_position.note, 
                "nominations": nominations}
    else:
        return {'done': 1}

@login_required
def indicators(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    election_positions = Position.objects.annotate(announced_count=Count('nominationannouncement'))\
                                         .filter(announced_count__gte=2).order_by('entity', 'city')
    context = {'election_positions': election_positions}

    return render(request, 'voting/indicators.html', context)

@login_required
def list_votes_per_position(request, position_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    position = get_object_or_404(Position, pk=position_id)
    votes = VoteNomination.objects.filter(position=position)
    context = {'position': position, 'votes': votes}

    return render(request, 'voting/list_votes_per_position.html', context)

def announce_winners(request, entity):
    current_year = SACYear.objects.get_current()
    per_city = []
    for city_code, city_name in city_choices:
        positions = Position.objects.filter(entity=entity, city=city_code)
        per_city.append((city_name, positions))
    context = {'entity': entity, 'per_city': per_city}
    return render(request, 'voting/announce_winners.html', context)

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated():
            return User.objects.none()

        qs = User.objects.filter(is_active=True)

        if self.q:
            search_fields = [re.sub('^user__', '', field) for field in utils.BASIC_SEARCH_FIELDS]
            print search_fields
            qs = utils.get_search_queryset(qs, search_fields, self.q)

        return qs

    def get_result_label(self, item):
        full_name = accounts.utils.get_user_ar_full_name(item) or item.username
        return"%s <bdi style='font-family: monospace;'>(%s)</bdi>" % (full_name, item.username)
