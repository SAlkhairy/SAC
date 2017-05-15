from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from voting import views as voting_views
from forms import NominationForm

urlpatterns = [
    url(r'^(?P<entity>(club|council))/$', voting_views.list_positions, name='list_positions'),
    url(r'^(?P<position_id>\d+)/add_nominee/$', voting_views.add_nominee, name='add_nominee'),
    url(r'^(?P<position_id>\d+)/(?P<nomination_id>\d+)/$', voting_views.show_nomination, name='show_nomination'),
    url(r'^(?P<position_id>\d+)/add_nominee/thanks/$', TemplateView.as_view(template_name='voting/nomination_thanks.html'), name='nomination_thanks'),
    url(r'^voting/ajax$', voting_views.handle_vote, name='handle_vote'),
    url(r'^voting/$', voting_views.show_voting_index, name='show_voting_index'),
    url(r'^voting/stats/$', voting_views.indicators, name='indicators'),    
    url(r'^voting/stats/(?P<position_id>\d+)/$', voting_views.list_votes_per_position, name='list_votes_per_position'),

    url(r'^announce_(?P<entity>(club|council))_nominees/$', voting_views.announce_nominees, name='announce_nominees'),

    # Obsolete
    url(r'^voting_closed/$', RedirectView.as_view(pattern_name="show_voting_index"), name='voting_closed'),

]
