from django.conf import settings
from django.http import HttpResponse

def whoosh_search_index(request):
     from whoosh.index import open_dir
     from whoosh.query import Every
     from whoosh.qparser import QueryParser
     from django.utils.html import escape

     query = request.GET.get("q")

     ix = open_dir(settings.HAYSTACK_CONNECTIONS['default']['PATH'])
     qp = QueryParser("text", schema=ix.schema)
     if query:
         q = qp.parse(query)
     else:
         q = Every("text")
     results = ix.searcher().search(q)
     output = "<ul>"
     for result in results:
         output += "<li>" + escape(str(result)) + "</li>"
     output += "</ul>"
     return HttpResponse(output)
