from sqlalchemy import create_engine, text
import os

database_connection_string = os.environ['DB_CONNECTION_STRING']
engine = create_engine(database_connection_string,
          connect_args = {
            "ssl": {
              "ssl_ca": "/etc/ssl/cert.pem"
            }
          }
                      )

def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    column_names = result.keys()
    jobs_list = [dict(zip(column_names, row)) for row in result.fetchall()]
    return jobs_list

def load_job_from_db(id):
    with engine.connect() as conn:
        query = text("SELECT * FROM jobs WHERE id = :val")
        result = conn.execute(query, {"val": id})
        row = result.fetchone()

    if row is None:
        return None
    else:
        column_names = result.keys()
        return dict(zip(column_names, row))




      
      