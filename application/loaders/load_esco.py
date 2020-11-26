import argparse
import logging
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from application.utils import parse_arguments

sys.path.append('../')
from application.settings import ENGINE_STRING

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class EscoLoader(object):
    """This class is used to load esco skills to DB"""

    def __init__(self, skills_file):
        self.skills_path = skills_file
        self.fields = ['skillType', 'preferredLabel', 'altLabels', 'description']

        self.engine = create_engine(ENGINE_STRING, poolclass=NullPool)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)

        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Skills = self.Base.classes.skills

    def load(self):
        """This function is used to load skills files"""
        skills_df = pd.read_csv(self.skills_path, usecols=self.fields)
        skills_df['skillType'] = skills_df['skillType'].map(
            lambda row: 1 if row in ['skill/competence', 'skill/competemce knowledge'] else 0)

        skills_table_exists = self.engine.has_table('skills')
        if skills_table_exists:
            for index, row in skills_df.iterrows():
                new_skill = self.Skills(
                    name=row['preferredLabel'],
                    alternative_labels=row['altLabels'],
                    hard_skill=row['skillType'],
                    description=row['description']
                )
                self.session.add(new_skill)
            self.session.commit()
        log.info("Esco skills loaded in DB")


if __name__ == '__main__':
    args = parse_arguments().parse_args()
    file_path = args.path
    if file_path:
        # 'C:/Users/pkapsalis.EPU/Desktop/skills_en.csv'
        es = EscoLoader(skills_file=file_path)
        es.load()
