from __future__ import division

from django_conneg.views import HTMLView
import rdflib

from humfrey.utils.views import RedisView
from humfrey.results.views.standard import RDFView, ResultSetView
from humfrey.utils.namespaces import NS
from humfrey.sparql.views import StoreView
from humfrey.linkeddata.resource import Resource
from humfrey.linkeddata.views import MappingView

class DatasetView(StoreView, MappingView, RDFView, HTMLView):
    catalog = rdflib.URIRef("https://data.ox.ac.uk/id/dataset/catalogue")

    query = """
        DESCRIBE {catalog} ?dataset ?license ?publisher ?contact WHERE {{
            {catalog} dcat:dataset ?dataset .
            ?dataset a void:Dataset .
            OPTIONAL {{ ?dataset dcterms:license ?license }} .
            OPTIONAL {{ ?dataset dcterms:publisher ?publisher }} .
            OPTIONAL {{ ?dataset oo:contact ?contact }} .
        }}""".format(catalog=catalog.n3())

    def get(self, request):
        graph = self.endpoint.query(self.query)
        datasets = graph.subjects(NS['rdf'].type, NS['void'].Dataset)
        datasets = [Resource(uri, graph, self.endpoint) for uri in datasets]
        datasets.sort(key=lambda ds:unicode(ds.label))

        context = {
            'graph': graph,
            'datasets': datasets,
        }

        return self.render(request, context, 'datasets')

EXAMPLES = (
    {'slug': 'science-area',
     'name': 'Science Area Map',
     'description': 'A re-imagining of <a href="http://www.ox.ac.uk/visitors_f'
       + 'riends/maps_and_directions/science_area.html">the official science a'
       + 'rea map</a> using OpenStreetMap and OxPoints data.'},
#    {'slug': 'openmeters',
#     'name': 'OpenMeters',
#     'description': "Graphical representations of the University of Oxford's electricity usage."},
    {'slug': 'vacancy-treemap',
     'name': 'Vacancy Treemap',
     'description': 'The distribution of job vacancies across the University.'},
#	{'slug': 'unicard-explorer',
#     'name': 'University Card Explorer',
#     'description': 'A tool for exploring statistics about University Card holders.'},
)

class ExploreView(HTMLView, RedisView):
    def get(self, request):
        context = {
            'examples': EXAMPLES,
        }
        return self.render(request, context, 'explore')

class ExampleResourceView(ResultSetView, HTMLView, StoreView, MappingView):
    _QUERY = """
        CONSTRUCT {
            ?dataset a void:Dataset ;
              rdfs:label ?datasetLabel ;
              void:exampleResource ?resource .
            ?resource ?p ?resourceLabel .
        } WHERE {
            ?dataset a void:Dataset ;
              rdfs:label ?datasetLabel ;
              void:exampleResource ?resource .
            ?resource ?p ?resourceLabel .
            FILTER (?p in (rdfs:label, dc:title, dcterms:title, foaf:name)) .
        }"""

    def get(self, request):
        graph = self.endpoint.query(self._QUERY)
        context = {
            'graph': graph,
            'subjects': [Resource(uri, graph, self.endpoint) for uri in graph.subjects(NS.rdf.type, NS.void.Dataset)],
        }

        return self.render(request, context, 'explore-resource')

class ExampleQueryView(ResultSetView, HTMLView, StoreView, MappingView):
    _QUERY = """
        SELECT ?dataset ?datasetLabel ?value ?label ?comment WHERE {
            ?dataset a void:Dataset ;
              rdfs:label ?datasetLabel ;
              oo:exampleQuery [
                rdf:value ?value ;
                rdfs:label ?label ;
                rdfs:comment ?comment ]
        }"""

    def get(self, request):
        context = {
            'results': self.endpoint.query(self._QUERY),
        }

        return self.render(request, context, 'explore-query') 

class ExampleDetailView(HTMLView):
    def get(self, request, slug):
        return self.render(request, {}, 'examples/%s' % slug)

class ForbiddenView(HTMLView):
    template_name = 'forbidden'
    _force_fallback_format = 'html'
    
    def dispatch(self, request):
        self.context = {'status_code': 403}
        setattr(self, request.method.lower(), self.render)
        return super(ServerErrorView, self).dispatch(request)

class ServerErrorView(HTMLView):
    template_name = '500'
    _force_fallback_format = 'html'
    
    def dispatch(self, request):
        self.context = {'status_code': 500}
        setattr(self, request.method.lower(), self.render)
        return super(ServerErrorView, self).dispatch(request)
