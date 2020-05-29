import logging
import sys

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

sys.path.append('../')
from settings import ENGINE_STRING

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class PostgresLoader(object):
    """
    This is a Python Object that handles Postgress DB using SQLAlchemy
    """

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.Base = automap_base()
        self.base = self.Base.prepare(self.engine, reflect=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Courses = self.Base.classes.courses
        self.Skills = self.Base.classes.skills

    def load_courses_to_flask_model_tables(self):
        """Populate flask model table for courses"""

        log.info("Populating Course table")

        table_exists = self.engine.has_table('courses')
        if table_exists:
            self.pass_courses()
            log.info("Table saved to Postgres")

    def load_skills_to_flask_model_tables(self):
        """Populate flask model table for skills"""

        log.info("Populating Skills table")

        table_exists = self.engine.has_table('skills')
        if table_exists:
            self.pass_skills()
            log.info("Table saved to Postgres")

    def pass_courses(self):
        """This function is used to pass courses from curriculum_designer_courses table to courses table"""

        cd = pd.read_sql_table('curriculum_designer_course', self.engine)

        for index, row in cd.iterrows():
            new_course = self.Courses(id=row['id'],
                                      name=row['course_title'],
                                      description=row['course_description'],
                                      semester=row['course_semester'],
                                      startDate='1-09-2000',
                                      endDate='28-05-2020',
                                      updatedDate='28-05-2020',
                                      events=[{"name": "event1"}, {"name": "event2"}, {"name": "ev3"}]
                                      )
            self.session.add(new_course)
        self.session.commit()

    def pass_skills(self):
        """This function is used to pass courses from curriculum_designer_skills table to skills table"""

        sd = pd.read_sql_table('skills_courses_table', self.engine)

        for index, row in sd.iterrows():
            new_skill = self.Skills(name=row['skill_title'], course_id=row['course_id'])
            self.session.add(new_skill)
        self.session.commit()

    def delete_data(self):
        """This function is used to remove existing data in courses and skills tables"""

        self.session.query(self.Skills).delete()
        log.info("Skills data removed")

        self.session.query(self.Courses).delete()
        log.info("Courses data removed")

        self.session.commit()


def main():
    postgres_loader = PostgresLoader()
    postgres_loader.delete_data()

    postgres_loader.load_courses_to_flask_model_tables()
    log.info("NTUA Courses data transferred to courses table")

    postgres_loader.load_skills_to_flask_model_tables()
    log.info("NTUA Skills data transferred to skills table")


if __name__ == "__main__":
    main()
