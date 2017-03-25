from django.conf.urls import url, include

from voting import views as voting_views
from forms import NominationForm

urlpatterns = [

    url(r'^$', voting_views.list_positions, name='list_positions'),
    url(r'^(?P<position_id>\d+)/add_nominee', voting_views.add_nominee, name='add_nominee'),


]
