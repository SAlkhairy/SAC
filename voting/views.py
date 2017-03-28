from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Position, Nomination
from .forms import NominationForm

def show_index(request):
    if request.user.is_authenticated():
        return render(request, 'accounts/home.html')
    else:
        return render(request, 'accounts/home_unauthenticated.html')

@login_required
def list_positions(request, entity):
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
    position = get_object_or_404(Position, pk=position_id)
    if request.method == 'POST':
        instance = Nomination(user=request.user, position=position)
        form = NominationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            print instance.pk
            return HttpResponseRedirect(reverse("voting:nomination_thanks", args=(position.pk,)))
    elif request.method == 'GET':
        form = NominationForm()
    context = {'form': form,
               'position': position}
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

