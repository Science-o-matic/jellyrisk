from django.contrib import admin
from django.utils.translation import ugettext as _

from models import *

class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]

    def queryset(self, request):
        return EventCategory.on_site.all()

    def save_model(self, request, obj, form, change):
        obj.save()
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        if current_site not in obj.sites.all():
            obj.sites.add(current_site)

admin.site.register(EventCategory, EventCategoryAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start', 'category_list']
    list_filter = ['start', 'categories',]
    search_fields = ['name', 'description', 'location']
    date_hierarchy = 'start'
    filter_horizontal = ['categories']
    fieldsets = (
        ('Event info',{
            'fields': ('name', 'start', 'description'),
        }),
        (_(u'More options...'),{
            'classes': ['collapse'],
            'fields': ('location', 'time', 'end', 'categories'),
        }),
    )
    
    # Descomentar para usar tinymce en el administrador.
    #~ def formfield_for_dbfield(self, db_field, **kwargs):
        #~ from django.core.urlresolvers import reverse
        #~ from tinymce.widgets import TinyMCE
        #~ if db_field.name == 'description':
            #~ return db_field.formfield(widget=TinyMCE(
            #~ attrs={'cols': 80, 'rows': 30},
                #~ mce_attrs={'external_link_list_url': reverse('tinymce.views.flatpages_link_list')},
            #~ ))
        #~ return super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        
    def queryset(self, request):
        return Event.on_site.all()
	
    def save_model(self, request, obj, form, change):
        obj.save()
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        if current_site not in obj.sites.all():
            obj.sites.add(current_site)

admin.site.register(Event, EventAdmin)
