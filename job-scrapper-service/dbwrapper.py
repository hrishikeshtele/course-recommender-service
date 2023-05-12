import psycopg2


class DBActions:
    connection = None

    def __init__(self):
        self.connection = psycopg2.connect(
            host='',
            port='',
            user='',
            password='',
            database=''
        )
        cursor = self.connection.cursor()

        # Creating table as per requirement
        create_table_sql = '''CREATE TABLE IF NOT EXISTS jobs_to_skills(
                                jobs_to_skills_id SERIAL PRIMARY KEY,
                                job_title VARCHAR(255) NOT NULL,
                                location VARCHAR(50),
                                skills VARCHAR(255))'''

        cursor.execute(create_table_sql)

    def add_to_db(self, job_title: str, location: str, skills: str):
        cursor = self.connection.cursor()
        insert_sql = ''' insert into jobs_to_skills(job_title, location, skills) values('%s', '%s', '%s')''' % (
            job_title, location, skills)
        cursor.execute(insert_sql)
        self.connection.commit()

    def record_exists(self, job_title):
        cur = self.connection.cursor()
        cur.execute("SELECT job_title FROM jobs_to_skills WHERE job_title = %s", (job_title,))
        return cur.fetchone() is not None

    def get_record(self, job_title):
        cur = self.connection.cursor()
        cur.execute("SELECT * FROM jobs_to_skills WHERE job_title = %s", (job_title,))
        return cur.fetchone()
