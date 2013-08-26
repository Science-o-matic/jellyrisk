from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

urlpatterns += patterns('',
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
        {'url': settings.STATIC_URL + 'img/favicon.ico'}),
    url(r'^gallery/', include('imagestore.urls', namespace='imagestore')),
    url(r'^store-locator/', include('store_locator.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^search/', include('haystack.urls')),
    (r'^tinymce/', include('tinymce.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^wix/', 'jellyrisk_site.views.whoosh_search_index'),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
