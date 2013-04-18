from django.conf.urls.defaults import *
from models import Event

event_dict = {
	'queryset': Event.on_site.all(),
	'template_object_name': 'event'
}

urlpatterns = patterns('',
    url(r'^$', 'simple_events.views.events', name="events"),
    url(r'^(?P<year>\d{4})/(?P<month>\d+)/(?P<day>\d+)/$','simple_events.views.events_day', name="events_day"),
)
urlpatterns += patterns('django.views.generic',
	url(r'^event-(?P<object_id>\d+)/$', 'list_detail.object_detail', event_dict, name="event_detail"),
)
