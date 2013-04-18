import mimetypes, os
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotModified, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.static import was_modified_since
from django.utils.http import http_date
from django.views.decorators.cache import never_cache
from django.db import transaction
from django.utils.encoding import smart_str
from models import *
from datetime import date


#Utils --------------------------------------------------

def render_to_response(request, template_name, context_dict = {}):
    from django.template import RequestContext
    from django.shortcuts import render_to_response as _render_to_response
    context = RequestContext(request, context_dict)
    return _render_to_response(template_name, context_instance=context)


def render_to(template_name):
    def renderer(func):
        @never_cache
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
            return render_to_response(request, template_name, output)
        return wrapper
    return renderer

def get_user_doc_or_404(request, doc_id):
    try:
        return Document.objects.get(pk=doc_id, owner=request.user)
    except:
        raise Http404()
    

#Views --------------------------------------------------

@render_to('simple_events/events_archive.html')
def events(request):
    events = Event.objects.all()
    return locals()

@render_to('simple_events/events_archive.html')
def events_day(request, year, month, day):
    events = Event.objects.filter(start=date(int(year), int(month), int(day)))
    return locals()
