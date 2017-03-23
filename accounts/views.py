from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from forms import SignupForm

from userena import views as userena_views









# Create your views here.


#def signup_extra(request, signup_form, template_name):
#    if request.method == 'POST':
#        form = SignupForm(request.POST)
#        # extra_context for Userena's view
#        extra_context = {'form': form}
#        return userena_views.signup(request, extra_context=extra_context)###