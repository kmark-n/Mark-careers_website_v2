from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db
from flask_sqlalchemy import SQLAlchemy
import os
from flask_admin import Admin

admin=Admin()
db=SQLAlchemy()
def create_app():
  
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI']=os.environ['DB_CONNECTION_STRING']
  db.init_app(app)
  admin.init_app(app)
  
  
      
  @app.route("/")
  def mark_careers():
    jobs_list = load_jobs_from_db()
    return render_template('home.html', jobs = jobs_list)
  
  @app.route("/api/jobs")
  def list_jobs():
    jobs_list = load_jobs_from_db()
    return jsonify(jobs=jobs_list)
  
  @app.route("/job/<id>")
  def show_job(id):
    job = load_job_from_db(id)
    if not job:
      return "Not found", 404
    return render_template('jobpage.html', job = job)
  
  @app.route("/job/<id>/apply", methods=['post'])
  def apply_to_job(id):
    data = request.form
    job = load_job_from_db(id)
    add_application_to_db(id, data)
    return render_template('application_submitted.html', application=data, job = job)

  return app
    
    
    
if __name__ == "__main__":
  app=create_app()
  app.run(host='0.0.0.0', debug=True)