from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Position, Nomination
from .forms import NominationForm

def show_index(request):
    return render(request, 'accounts/home.html')

def list_positions(request, entity):
    if entity in ['club', 'council']:
        positions = Position.objects.filter(entity=entity)
    else:
        raise Http404

    context = {'positions': positions}
    return render(request, 'voting/list_' + entity + '_positions.html', context)

def add_nominee(request, position_id):
    position = get_object_or_404(Position, pk=position_id)
    if request.method == 'POST':
        instance = Nomination(user=user, position=position)
        form = NominationForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            context = {'form': form,
                       'position': position}
            return HttpResponseRedirect(reverse("voting:nomination_thanks"))
    elif request.method == 'GET':
        form = NominationForm()
        context = {'form': form,
                   'position': position}

    return render(request,'voting/add_nominee.html', context)
