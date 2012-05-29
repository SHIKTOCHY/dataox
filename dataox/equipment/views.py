import httplib
import urllib2
try:
    import json
except ImportError:
    import simplejson

from django_conneg.views import HTMLView, JSONPView
from django.conf import settings
from django.http import Http404
import rdflib

from humfrey.desc import views as desc_views
from humfrey.elasticsearch import views as elasticsearch_views
from humfrey.linkeddata.views import MappingView
from humfrey.results.views.standard import RDFView
from humfrey.sparql.views import StoreView, CannedQueryView
from humfrey.utils.namespaces import NS
from humfrey.utils.resource import BaseResource

from .forms import AdvancedSearchForm

class EquipmentView(object):
    """
    Mixin to choose between public and internal indexes.
    """

    @property
    def store_name(self):
        if self.request.user.groups.filter(name='member').count():
            return 'equipment'
        else:
            return 'public'

    @property
    def index_name(self):
        return '{0}/equipment'.format(self.store_name)

class DescView(EquipmentView, desc_views.DescView):
    pass

class DocView(EquipmentView, desc_views.DocView):
    template_name = 'equipment/view'

class SearchView(EquipmentView, elasticsearch_views.SearchView):
    @property
    def facets(self):
        facets = {
            'institution': {'terms': {'field': 'formalOrganisation.uri', 'size': 100}},
            'basedNear': {'terms': {'field': 'basedNear.uri', 'size': 100}},
            'category': {'terms': {'field': 'category.uri'}}
        }
        if 'filter.formalOrganisation.uri' in self.request.GET:
            facets['department'] = {'terms': {'field': 'equipmentOf.uri', 'size': 100}}
        if 'filter.category.uri' in self.request.GET:
            facets['subcategory'] = {'terms': {'field': 'subcategory.uri'}}
        return facets

        #          'oxford': {'terms': {'field': 'oxfordUniversityEquipment'}},

    template_name = 'equipment/search'

    dependent_parameters = {'filter.category.uri': ('filter.subcategory.uri',),
                            'filter.formalOrganisation.uri': ('filter.equipmentOf.uri',)}
    
    def finalize_context(self, request, context):
        if not context.get('q'):
            context['form'] = AdvancedSearchForm(request.GET or None,
                                                 search_url=self.search_url,
                                                 store=self.store)
        return context

#class ItemView(EquipmentView, HTMLView, JSONPView):
#    def get(self, request, id):
#        try:
#            url = ('http://%(host)s:%(port)s/%s/' % (settings.ELASTICSEARCH_SERVER, self.index_name)) + id
#            item = elasticsearch_views.SearchView.Deunderscorer(json.load(urllib2.urlopen(url)))
#        except urllib2.HTTPError, e:
#            if e.code == httplib.NOT_FOUND:
#                raise Http404
#            raise
#        
#        more_like_this_url = url + '/_mlt?min_doc_freq=1'
#        
#        context = {'item': item,
#                   'more_like_this': elasticsearch_views.SearchView.Deunderscorer(json.load(urllib2.urlopen(more_like_this_url)))}
#        
#        return self.render(request, context, 'equipment/item')

class BrowseView(EquipmentView, HTMLView, RDFView, CannedQueryView, MappingView):
    concept_scheme = rdflib.URIRef('http://data.ox.ac.uk/id/equipment-category')
    datatype = rdflib.URIRef('http://data.ox.ac.uk/id/notation/equipment-category')
    
    template_name = 'equipment/browse'
    
    @property
    def notation(self):
        if self.kwargs.get('notation'):
            return rdflib.Literal(self.kwargs['notation'], datatype=self.datatype)
    
    def get_query(self, request, notation):
        if self.notation:
            return """
                DESCRIBE ?concept ?narrower ?equipment ?narrowerEquipment WHERE {{
                  ?concept skos:notation {notation} .
                  OPTIONAL {{ ?equipment dcterms:subject ?concept }} .
                  OPTIONAL {{
                    ?concept skos:narrower ?narrower .
                    OPTIONAL {{ ?narrowerEquipment dcterms:subject ?narrower }}
                  }}
                }}""".format(notation=self.notation.n3())
        else:
            return """
                CONSTRUCT {{
                 {concept_scheme} a skos:ConceptScheme ;
                    skos:prefLabel ?conceptSchemeLabel ;
                    skos:hasTopConcept ?concept .
                  ?narrower a skos:Concept ;
                    skos:prefLabel ?conceptLabel ;
                    skos:notation ?conceptNotation ;
                    skos:narrower ?evenNarrower .
                }} WHERE {{
                  {concept_scheme} a skos:ConceptScheme ;
                    skos:prefLabel ?conceptSchemeLabel ;
                    skos:hasTopConcept ?concept .
                  ?concept skos:narrower* ?narrower .
                  ?narrower a skos:Concept ;
                    skos:prefLabel ?conceptLabel ;
                    skos:notation ?conceptNotation .
                  EXISTS {{
                    ?narrower skos:narrower*/^dcterms:subject ?equipment 
                  }} .
                  OPTIONAL {{
                    ?narrower skos:narrower ?evenNarrower .
                    EXISTS {{
                      ?evenNarrower skos:narrower*/^dcterms:subject ?narrowerEquipment
                    }}
                  }}
                }}""".format(concept_scheme=self.concept_scheme.n3())
                  # RT#1925559 GROUP BY ?concept ?conceptLabel ?conceptNotation ?narrower

    def finalize_context(self, request, context, notation):
        graph = context['graph']
        context['equipment'] = map(self.resource, graph.subjects(NS.rdf.type, NS.oo.Equipment))
        context['equipment'].sort(key=lambda s:s.label)
        if self.notation:
            concept = graph.value(None, NS.skos.notation, self.notation)
            if not concept:
                raise Http404
            context['concept'] = self.resource(concept)
            context['concepts'] = map(self.resource, graph.objects(concept, NS.skos.narrower))
            context['level'] = 'subcategory' if '/' in self.notation else 'category'
        else:
            context['concepts'] = map(self.resource, graph.objects(self.concept_scheme, NS.skos.hasTopConcept))
            context['level'] = 'index'
        context['concepts'].sort(key=lambda s:s.label)
        
        return context