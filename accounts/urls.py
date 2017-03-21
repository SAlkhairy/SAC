from django.conf.urls import url
from userena import views as userena_views
from forms import CustomSignupForm

urlpatterns = [
    #url(r'^signup/$', userena_views.signup, {'template_name': 'signup.html'}, name="signup"),
    url(r'^signup/$', userena_views.signup,{'signup_form': CustomSignupForm}),

]