from __future__ import with_statement
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import Event
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from calendar import HTMLCalendar, TimeEncoding, month_name, day_abbr

from django.utils.dates import MONTHS
from django.utils.dates import WEEKDAYS_ABBR

from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

import locale

class EventCalendar(HTMLCalendar):
    """http://journal.uggedal.com/creating-a-flexible-monthly-calendar-in-django"""
    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
                body = '<a class="tipsy" href="#" title="%s">%d</a>' % (_('Today'), day)
                if day in self.events:
                    d = reverse('events_day', args=(self.year, self.month, day))
                    body = '<a class="tipsy" href="%s" title="%s">%d</a>' % (d, _("Events found"), day)
                return self.day_cell(cssclass, body)

            if day in self.events:
                cssclass += ' filled'
                title = ['<ul class=event>']
                for event in self.events[day]:
                    title.append('<li><b>%s</b></li>' % esc(event.name))
                title.append('</ul>')
                d = reverse('events_day', args=(self.year, self.month, day))
                body = '<a class="tipsy" href="%s" title="%s">%d</a>' % (d, _("Events found"), day)
                return self.day_cell(cssclass, body)
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')
    
    def formatweekday(self, day):
        return '<th class="%s">%s</th>' % (self.cssclasses[day], WEEKDAYS_ABBR[day].title())

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (MONTHS[themonth].title(), theyear)
        else:
            s = '%s' % MONTHS[themonth].title()
        return '<tr><th colspan="7" class="month">%s</th></tr>' % s

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        field = lambda event: event.start.day
        return dict(
            [(day, list(items)) for day, items in groupby(events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


class CMSCalendarEventsPlugin(CMSPluginBase):
    
    name = _("Calendar Events")
    render_template = "simple_events/events_calendar.html"

    def render(self, context, instance, placeholder):
        today = date.today()
        year = today.year
        month = today.month

        request = context['request']
        if request.GET:
            month = int(request.GET.get('month') or month)
            year = int(request.GET.get('year') or year)
        first_day = date(year,month,1)
        if month == 12:
            last_day = date(year+1,1,1)
        else:
            last_day = date(year,month+1,1)
        events = Event.objects.filter(start__gte=first_day).filter(start__lt=last_day)
        cal = EventCalendar(events).formatmonth(year, month)
        context.update({'instance':instance,
                        'events': events,
                        'calendar': mark_safe(cal),
                        'placeholder':placeholder})
        return context

plugin_pool.register_plugin(CMSCalendarEventsPlugin)
