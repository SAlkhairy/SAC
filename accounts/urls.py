from django.conf.urls import url, include
from userena import views as userena_views
from userena.forms import AuthenticationForm
from accounts import views as account_views
from .forms import CustomSignupForm, ModifiedAuthenticationForm

urlpatterns = [
    url(r'^signup/$', userena_views.signup, {'signup_form': CustomSignupForm, 'template_name': 'accounts/signup.html'}, name="signup"),
    url(r'^signin/$', userena_views.signin, {'auth_form': ModifiedAuthenticationForm}),
    url(r'^', include('userena.urls')),


]
