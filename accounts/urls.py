from django.conf.urls import url
from userena import views as userena_views
from accounts import views as account_views
from forms import CustomSignupForm

urlpatterns = [
    url(r'^signup/$', account_views.signup_extra, {'signup_form': CustomSignupForm, 'template_name': 'accounts/signup.html'}, name="signup"),

]
