import logging
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

sys.path.append('../')
from application.settings import ENGINE_STRING, CURRICULUM_DB_ENGINE, STR_CURRENT_TIME

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
        self.SkillToCourse = self.Base.classes.skills_courses

    def load_data_to_flask_model_tables(self):
        """Populate flask model table for courses"""

        log.info("Populating Course table")

        courses_table_exists = self.engine.has_table('courses')
        if courses_table_exists:
            self.pass_courses_data()
            log.info("Table saved to Postgres")

        log.info('Populating Skills Table')

        skills_table_exists = self.engine.has_table('skills')
        if skills_table_exists:
            self.pass_skills_data()
            log.info("Table saved to Postgres")

        skills_courses_table_exists = self.engine.has_table('skills_courses')
        if skills_courses_table_exists:
            self.pass_skills_courses_relation()
            log.info("Table saved to Postgres")

    def pass_courses_data(self):
        """This function is used to pass courses from curriculum_designer_courses table to courses table"""

        designer_courses = pd.read_sql_table('curriculum_designer_course', CURRICULUM_DB_ENGINE)[
            ['id', 'course_title', 'course_description', 'course_semester']]

        for index, row in designer_courses.iterrows():
            new_course = self.Courses(id=row['id'],
                                      name=row['course_title'],
                                      description=row['course_description'],
                                      semester=row['course_semester'],
                                      updatedDate=STR_CURRENT_TIME,
                                      events=[{"name": "event1"}, {"name": "event2"}, {"name": "ev3"}]
                                      )
            self.session.add(new_course)
        self.session.commit()

    def pass_skills_data(self):
        """Append skills data to Postgress"""
        designer_skills = pd.read_sql_table('curriculum_designer_skill', CURRICULUM_DB_ENGINE)

        for index, row in designer_skills.iterrows():
            new_skill = self.Skills(
                id=row['id'],
                name=row['skill_title'],
                type='tool',
                hard_skill=row['hard_skill']
            )
            self.session.add(new_skill)
        self.session.commit()

    def pass_skills_courses_relation(self):
        """This functions is used to transfer skills-courses relation to Postgres"""
        designer_skills_courses = pd.read_sql_table('skills_courses_table', CURRICULUM_DB_ENGINE)

        for index, row in designer_skills_courses.iterrows():
            skills_courses = self.SkillToCourse(
                skill_id=row['skill_id'],
                course_id=row['course_id']
            )
            self.session.add(skills_courses)
        self.session.commit()

    def delete_data(self):
        """This function is used to remove existing data in courses and skills tables"""
        self.session.query(self.SkillToCourse).delete()
        log.info("existing Skills <-> Course relations removed")

        self.session.query(self.Skills).delete()
        log.info("existing Skills data removed")

        self.session.query(self.Courses).delete()
        log.info("existing Courses data removed")

        self.session.commit()


def main():
    """Run this script to transfer NTUA Courses and Skills Information to Qualichain DB"""
    postgres_loader = PostgresLoader()
    postgres_loader.delete_data()

    postgres_loader.load_data_to_flask_model_tables()
    log.info("NTUA Curriculum Designer Data transferred to Courses/Skills/SkillsToCourses table")


if __name__ == "__main__":
    main()
