import logging
import os
import sys
import time

from rdflib import Graph
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

sys.path.append('../')
from application.settings import ENGINE_STRING

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class SaroLoader(object):
    """This Python object is used to load saro ttl skills"""

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Skills = self.Base.classes.skills

    @staticmethod
    def ttl_to_xml(ttl_path, output_path):
        """This function is used to transform a ttl file to xml"""
        ttl_grapg = Graph()
        ttl_grapg.parse(ttl_path, format='turtle')
        ttl_grapg.serialize(output_path, format='xml')

    def append_to_db(self, data):
        """This function is used to append data to DB"""
        new_skill = self.Skills(
            name=data['name'],
            type=data['type'],
            hard_skill=data['is_hard_skill'],
        )
        self.session.add(new_skill)
        self.session.commit()

    @staticmethod
    def parse_description(file_path):
        """This function is used to parse xml content"""
        with open(file_path, 'r') as saro_file:
            content = saro_file.read()
            bs_content = bs(content, "lxml")
            body = bs_content.select('body')
            all_description = body[0].find_all('rdf:description')
        return all_description

    def parse_informatic_skills(self):
        """This function is used to parse informatic skills from .ttl"""
        xml_info_skills = "loaders/saro_ttls/output_info_skills.xml"
        self.ttl_to_xml(ttl_path='loaders/saro_ttls/informaticSkills.ttl', output_path=xml_info_skills)
        log.info("Process {}".format(xml_info_skills))
        all_description = self.parse_description(file_path=xml_info_skills)

        for description in all_description:
            informatic_skill = description.find('rdfs:label').text
            type = "informaticSkills"

            skill_type = description.find('rdf:type')
            is_hard_skill = False
            if skill_type:
                skill_type = skill_type['rdf:resource'].replace('http://w3id.org/saro#', '')
                if skill_type == 'Sector':
                    continue
                if skill_type == 'Tool' or skill_type == 'Product':
                    is_hard_skill = True
                if skill_type == "Skill":
                    has_skill_type = description.find('saro:hasskilltype').text
                    if has_skill_type == 'knowledge':
                        is_hard_skill = False
                    else:
                        is_hard_skill = True
                if skill_type == 'Topic':
                    is_hard_skill = False
                if skill_type == 'ComplexSkill':
                    is_hard_skill = True
                new_skill_data = {'name': informatic_skill, 'type': type, 'is_hard_skill': is_hard_skill}
                self.append_to_db(new_skill_data)

    def parse_generic_ttl_data(self, output_xml_path, skills_type):
        """This function is a generic parser"""
        all_description = self.parse_description(file_path=output_xml_path)
        log.info("Process {}".format(output_xml_path))
        for sample in all_description:
            is_from_esco = sample.find('saro:isfrom')
            if is_from_esco:
                label = sample.find('rdfs:label').text
                skill_type = sample.find('saro:hasskilltype').text
                if skill_type == 'skill':
                    is_hard_skill = True
                else:
                    is_hard_skill = False
                data = {'name': label, 'is_hard_skill': is_hard_skill, 'type': skills_type}
                self.append_to_db(data)

    def process_generic_ttl_files(self):
        """This function is used to parse generic ttl files"""
        loaders_base_dir = 'loaders/saro_ttls/'
        generic_ttl_files = {
            'businessAdministrationSkills': os.path.join(loaders_base_dir, 'businessAdministrationSkills.ttl'),
            'LegalSocialCulturalSkills': os.path.join(loaders_base_dir, 'LegalSocialCulturalSkills.ttl'),
            'TeachingSkills': os.path.join(loaders_base_dir, 'TeachingSkills.ttl')
        }
        for file_key in generic_ttl_files.keys():
            output_xml = os.path.join(loaders_base_dir, '{}.xml'.format(file_key))
            self.ttl_to_xml(
                ttl_path=generic_ttl_files[file_key],
                output_path=output_xml
            )
            self.parse_generic_ttl_data(output_xml_path=output_xml, skills_type=file_key)

    def process_travesal_skills(self):
        """This function is used to process travesal skills content"""
        travesal_skills_path = 'loaders/saro_ttls/TransversalSkills.ttl'
        travesal_skills_xml = 'loaders/saro_ttls/TransversalSkills.xml'
        self.ttl_to_xml(ttl_path=travesal_skills_path, output_path=travesal_skills_xml)
        log.info("Process {}".format(travesal_skills_xml))

        all_description = self.parse_description(travesal_skills_xml)
        for description in all_description:
            skills_type = 'TransversalSkills'
            is_hard_skill = False
            label = description.find('rdfs:label').text
            data = {'name': label, 'is_hard_skill': is_hard_skill, 'type': skills_type}
            self.append_to_db(data)


if __name__ == '__main__':
    sload = SaroLoader()
    sload.parse_informatic_skills()
    sload.process_generic_ttl_files()
    sload.process_travesal_skills()
