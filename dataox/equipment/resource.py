from humfrey.linkeddata.resource import ResourceRegistry

import dataox.resource

class Equipment(object):
    types = ('oo:Equipment',)

    @classmethod
    def _describe_patterns(cls):
        return [
            '%(uri)s oo:contact %(contact)s . OPTIONAL { %(contact)s v:tel %(telephone)s }',
            '%(uri)s oo:accessPrerequisite %(accessPrerequisite)s',
            '%(uri)s oo:useRestriction %(useRestriction)s',
            '%(uri)s oo:availability %(availability)s',
            '%(uri)s dcterms:subject %(category)s',
            
            '%(uri)s oo:equipmentOf %(department)s',
            '%(uri)s foaf:based_near %(basedNear)s',
            '%(uri)s spatialrelations:within %(within)s',
            '%(uri)s gr:hasMakeAndModel %(makeAndModel)s . %(makeAndModel)s gr:hasManufacturer %(manufacturer)s',
        ]
        
    @property
    def geo_provider(self):
        return self.spatialrelations_within or self.foaf_based_near
    
    @property
    def geo_lat(self):
        return self.geo_provider.geo_lat if self.geo_provider else None

    @property
    def geo_long(self):
        return self.geo_provider.geo_long if self.geo_provider else None

class Organization(dataox.resource.oxpoints.Organization):
    @classmethod
    def _describe_patterns(cls):
        return [
            '%(equipment)s oo:equipmentOf %(uri)s',
        ]

resource_registry = dataox.resource.resource_registry + ResourceRegistry(
    Equipment, Organization
)
