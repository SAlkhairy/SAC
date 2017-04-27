from django.conf.urls import url, include
from django.views.generic import TemplateView

from voting import views as voting_views
from forms import NominationForm

urlpatterns = [
    url(r'^(?P<entity>(club|council))/$', voting_views.list_positions, name='list_positions'),
    url(r'^(?P<position_id>\d+)/add_nominee/$', voting_views.add_nominee, name='add_nominee'),
    url(r'^(?P<position_id>\d+)/(?P<nomination_id>\d+)/$', voting_views.show_nomination, name='show_nomination'),
    url(r'^(?P<position_id>\d+)/add_nominee/thanks/$', TemplateView.as_view(template_name='voting/nomination_thanks.html'), name='nomination_thanks'),
    url(r'^closed/$', TemplateView.as_view(template_name="voting/closed.html"), name='closed'),
    url(r'^announce_(?P<entity>(club|council))_nominees/$', voting_views.announce_nominees, name='announce_nominees'),

]
