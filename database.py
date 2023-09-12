from sqlalchemy import create_engine, text
from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv())

db_connection_string = os.getenv("DATABASE_URL")
print(db_connection_string)

engine = create_engine(
    db_connection_string,
    connect_args = {
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
    }
})


def load_job_from_db():
  with engine.connect() as conn:
    result = conn.execute(
      text("select * from applications"),
    )
    rows = result.all()
    # print(rows)
    myRow = rows[0]._mapping
    if len(rows) == 0:
      return None
    else:
      print(myRow['song_artist'])

load_job_from_db()
# def add_application_to_db(job_id, data):
#   with engine.connect() as conn:
#     query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education," +  
#                  " work_experience, resume_url) VALUES(:job_id, :full_name, :email, :linkedin_url, " + 
#                  ":education, :work_experience, :resume_url)")

#     values={'job_id': job_id,
#             'full_name':data['full_name'],
#             'email':data['email'],
#             'linkedin_url':data['linkedin_url'],
#             'education':data['education'],
#             'work_experience':data['work_experience'],
#             'resume_url':data['resume_url']
#             }
#     # for some reason I have to use a dictionary ad Values and stil create all those variables in the query stmt
#     # don't know why but i'll have to do this for now lol
#     conn.execute(
#       query,
#       values
#       # job_id=job_id,
#       # full_name=data['full_name'],
#       # linkedin_url=data['linkedin_url'],
#       # email=data['email'],
#       # education=data['education'],
#       # work_experience=data['work_experience'],
#       # resume_url=data['resume_url']
#     )
  