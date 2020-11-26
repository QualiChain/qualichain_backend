import os

import pandas
import tempfile

import sqlalchemy

CURRICULUM_DB = {
    "USER": os.environ.get('CDB_USER', "admin"),
    "PASSWORD": os.environ.get('CDB_PASSWORD', "admin"),
    "HOST": os.environ.get('CDB_HOST', 'qualichain.epu.ntua.gr'),
    "DATABASE": os.environ.get('CDB_DATABASE', 'api_db')
}
CURRICULUM_DB_ENGINE = "postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}/{DATABASE}".format(**CURRICULUM_DB)


def read_sql_tmpfile(query, db_engine):
    with tempfile.TemporaryFile() as tmpfile:
        copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
            query=query, head="HEADER"
        )
        conn = db_engine.raw_connection()
        cur = conn.cursor()
        cur.copy_expert(copy_sql, tmpfile)
        tmpfile.seek(0)
        cur.close()
        df = pandas.read_csv(tmpfile)
        return df

db = sqlalchemy.create_engine(CURRICULUM_DB_ENGINE)
my_query = "SELECT id, course_name FROM curriculum_designer_course"
df = read_sql_tmpfile(my_query, db)
db.dispose()
print(df)
