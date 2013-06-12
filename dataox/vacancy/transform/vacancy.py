# -*- coding: utf-8 -*-
from __future__ import with_statement

import datetime
import itertools
import logging

import dateutil.parser
from django.conf import settings
import pytz
from humfrey.update.transform.base import Transform
from humfrey.streaming import RDFXMLSerializer

from ..scraper import RecruitOxScraper, JobsAcScraper
from ..files import VacancyFileHandler
from ..models import Vacancy, Document

logger = logging.getLogger(__name__)

class RetrieveVacancies(Transform):
    vacancy_base_uri = 'https://data.ox.ac.uk/id/vacancy/'

    site_timezone = pytz.timezone(settings.TIME_ZONE)


    #save_directory = "c:\\documents and settings\\orie2163\\my documents\\python\\jobs\\"
    #job_directory = "c:\\documents and settings\\orie2163\\my documents\\python\\jobs\\%s\\"

    def __init__(self, current_transform, archive_transform):
        self.current_transform = current_transform
        self.archive_transform = archive_transform

        self.scrapers = (RecruitOxScraper, JobsAcScraper)
        self.file_handler = VacancyFileHandler()

    def execute(self, transform_manager):
        scrapers = [scraper(transform_manager) for scraper in self.scrapers]
        
        logger.info("Importing vacancies")
        changed = False

        for scraper in scrapers:
            changed = scraper.import_vacancies() or changed
            
        documents = Document.objects.filter(local_url='').select_related('vacancy')
        if documents:
            logger.info("Finished importing vacancies; retrieving %d new documents", documents.count())
            file_handler = VacancyFileHandler()
            for document in documents:
                try:
                    changed = file_handler.retrieve(document) or changed
                except Exception:
                    logger.exception("Could not retrieve file: %s", document.url)
            logger.info("Finished retrieving documents; starting to serialize")

        if not changed:
            logger.info("Nothing changed; we're done here.")
            return

        transforms = {'current': {'file': open(transform_manager('rdf'), 'w'),
                                  'transform': self.current_transform,
                                  'vacancies': []},
                      'archive': {'file': open(transform_manager('rdf'), 'w'),
                                  'transform': self.archive_transform,
                                  'vacancies': []}}

        for transform in transforms.values():
            transform['serializer'] = RDFXMLSerializer(transform['file'])

        for vacancy in Vacancy.objects.all():
            opening_date, closing_date = map(dateutil.parser.parse, (vacancy.opening_date, vacancy.closing_date))
            if opening_date < self.site_timezone.localize(datetime.datetime.now()) < closing_date:
                transforms['current']['vacancies'].append(vacancy)
            else:
                transforms['archive']['vacancies'].append(vacancy)

        for name, transform in transforms.items():
            triples = itertools.chain(*[v.triples(self.vacancy_base_uri) for v in transform['vacancies']])
            RDFXMLSerializer(triples).serialize(transform['file'])
            logger.debug("Finished serializing %s graph (%d bytes)", name, transform['file'].tell())
            transform['file'].close()

            transform['transform'].execute(transform_manager, transform['file'].name)
