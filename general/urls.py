from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from general import views as general_views

urlpatterns = [
    url(r'^static/(?P<page_id>\w+)/$', general_views.show_page, name='show_page'),
    url(r'^add_feedback/$', general_views.add_feedback, name='add_feedback'),
    url(r'^news/$', general_views.show_news, name='show_news'),
]