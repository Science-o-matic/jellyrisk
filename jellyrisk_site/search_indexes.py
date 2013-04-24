from django.conf import settings
from django.utils.translation import string_concat, ugettext_lazy
from haystack import indexes
from cms.models.managers import PageManager
from cms.models.pagemodel import Page
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class EnglishPageIndex(indexes.SearchIndex, indexes.Indexable):
    lang = 'en'

    text = indexes.CharField(document=True, use_template=False)
    pub_date = indexes.DateTimeField(model_attr='publication_date')
    login_required = indexes.BooleanField(model_attr='login_required')
    url = indexes.CharField(stored=True, indexed=False, model_attr='get_absolute_url')
    title = indexes.CharField(stored=True, indexed=False, model_attr='get_title')

    def get_model(self):
        return Page

    def prepare(self, obj):
         self.prepared_data = super(EnglishPageIndex, self).prepare(obj)
         text = ''
         for placeholder in obj.placeholders.all():
             for plugin in placeholder.cmsplugin_set.all():
                 instance, _ = plugin.get_plugin_instance()
                 if instance and instance.plugin_type == 'TextPlugin':
                     text += " %s" % (strip_tags(instance.body))
         self.prepared_data['text'] = text
         return self.prepared_data

    def index_queryset(self, using):
        return Page.objects.published().filter(title_set__language=self.lang).distinct()
