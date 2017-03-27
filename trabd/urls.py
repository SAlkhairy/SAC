from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from accounts import urls as accounts_urls
from voting import urls as voting_urls
from voting import views as voting_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', voting_views.show_index, name='home'),
    url(r'^accounts/', include(accounts_urls)),
    url(r'^positions/', include(voting_urls, namespace="voting")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
