from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators import csrf
from .models import SACYear, Position, Nomination
from .forms import NominationForm
from . import decorators
import StringIO
import qrcode
import qrcode.image.svg

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

def announce_nominees(request):
    current_year = SACYear.objects.get_current()
    context = {'sacyear': current_year}
    if current_year.is_announcement_due():
        nominations = Nomination.objects.filter(is_rejected=False,)
        context['nominations'] = nominations
    return render(request, 'voting/announce_nominees.html', context)



@login_required
def show_voting_index(request):
    current_year = SACYear.objects.get_current()
    if not current_year.is_voting_open():
        return HttpResponseRedirect(reverse("voting:voting_closed"))
    else:
        qrcode_output = StringIO.StringIO()
        qrcode.make("aaaa", image_factory=qrcode.image.svg.SvgImage, version=3).save(qrcode_output)
        qrcode_value = "".join(qrcode_output.getvalue().split('\n')[1:])

        return render(request,'voting/show_voting.html', {"qrcode_value": qrcode_value})

@login_required
@decorators.ajax_only
@decorators.post_only
@csrf.csrf_exempt
def handle_vote(request):
    if 'nomination_pk' in request.POST:
        pass
        # nomation =
        # VoteNomination.objects.create

    # {"position_name": ,
    #    "nomiations": [{"pk": ,
    #                     "nominee_name": },
    #                     ]}
    return {"position_name": "Vice President of the Student Club"}
