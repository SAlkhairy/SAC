from django.conf.urls import url, include

from voting import views as voting_views
from forms import NominationForm

urlpatterns = [

    url(r'^add_nominee/(?P<position_id>\d+)', voting_views.add_nominee, name='add_nominee'),


]
