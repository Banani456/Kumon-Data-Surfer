from flask import Flask, render_template, send_from_directory, request, session
from functions import*
import pandas as pd
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='templates', static_folder='output')


@app.route('/')
def index():
  return render_template('index.html')

@app.route("/submitted", methods=['POST', 'GET'])
def submitted():
  f = request.files['data']
  omit = request.files['unsubscribed']
  f.save(secure_filename(f.filename))
  omit.save(secure_filename(omit.filename))

  r = True
  m = True
  p = True
  a = True
  d = True
  
  # Uploaded File Path
  data_file_path = session.get('f.filename', None)
  strfilepath = str(f.filename)

  omit_file_path = session.get('omit.filename', None)
  stromitpath = str(omit.filename)
  #read csv
  uploaded_df = pd.read_csv(f.filename, encoding='unicode_escape')
  uploaded_omit = pd.read_csv(omit.filename, encoding='unicode_escape')

  database = omit_unsubscribed(uploaded_df, uploaded_omit)

  #Reading or Math requests
  select = request.form.get('rorm')
  if (select == 'r'):
    m = False
  elif(select== 'm'):
    r = False

  #K-level requests
  kltemp = request.form['kumonlevel']
  kl = kltemp.upper()

  #Active or Disc
  select = request.form.get('enroll')
  if (select == 'p'):
    p = True
    a = False
    d = False
  elif (select == 'a'):
    p = False
    d = False
    a = True
  elif(select== 'd'):
    p = False
    a = False
    d = True
  elif (select == 'pa'):
    d = False
    p = True
    a = True
  elif (select == 'pd'):
    a = False
    p = True
    d = True
  elif (select == 'ad'):
    p = False
    a = True
    d = True
  elif (select == 'pad'):
    p = True
    a = True
    d = True

  #Gradelevels
  stg = request.form.get('sgrade')
  eng = request.form.get('egrade')

  #birthdays
  stemp = request.form['sd']
  sdate = dt.strptime(stemp, "%Y-%m-%d").strftime("%m/%d/%Y")
  etemp = request.form['ed']
  edate = dt.strptime(etemp, "%Y-%m-%d").strftime("%m/%d/%Y")
 
  #call and return
  returncsv(birthday(sdate,edate,stg,eng,p,a,d,kl,r,m,database))
  clearcsv(strfilepath)
  clearcsv(stromitpath)
  return send_from_directory('output','return.csv')

app.run(host='0.0.0.0', port=81)


#data = pd.read_csv('Sample.csv')
#returncsv(readingOrMath(False, True, data))
