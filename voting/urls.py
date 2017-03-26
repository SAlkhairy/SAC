from django.conf.urls import url, include
from django.views.generic import TemplateView

from voting import views as voting_views
from forms import NominationForm

urlpatterns = [
    url(r'^(?P<entity>(club|council))/$', voting_views.list_positions, name='list_positions'),
    url(r'^(?P<position_id>\d+)/add_nominee/$', voting_views.add_nominee, name='add_nominee'),
    url(r'^(?P<position_id>\d+)/add_nominee/thanks/$', TemplateView.as_view(template_name='voting/nomination_thanks.html'), name='nomination_thanks')
]
