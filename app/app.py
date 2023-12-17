from sqlalchemy import create_engine, inspect, text
import sqlalchemy
import os
from dotenv import load_dotenv 
from flask import Flask, render_template, request, url_for, redirect, session
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from db_functions import update_or_create_user, get_db

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connection string
connect_args={'ssl':{'fake_flag_to_enable_tls': True}}
conn_string = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}")
engine = create_engine(conn_string)

app = Flask(__name__)
app.secret_key =os.urandom(12)
oauth = OAuth(app)
get_db()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/google/')
def google():
    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    redirect_uri = url_for('google_auth', _external=True)
    print('REDIRECT URL: ', redirect_uri)
    session['nonce'] = generate_token()
    redirect_uri = 'https://5000-cs-719093013193-default.cs-us-east1-pkhd.cloudshell.dev/google/auth/'
    return oauth.google.authorize_redirect(redirect_uri, nonce=session['nonce'])

@app.route('/google/auth/')
def google_auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token, nonce=session['nonce'])
    session['user'] = user
    update_or_create_user(user)
    print(" Google User ", user)
    return redirect('/patients')

@app.route('/patients')
def patients():
    user = session.get('user')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    patient_id = request.args.get('patient_id')
    date_of_birth = request.args.get('date_of_birth')
    if user:
        with engine.connect() as connection:
            if first_name:
                query_1 = text('SELECT * FROM patient_info WHERE first_name = :first_name')
                result_1 = connection.execute(query_1, {"first_name": first_name})
            elif last_name:
                query_1 = text('SELECT * FROM patient_info WHERE last_name = :last_name')
                result_1 = connection.execute(query_1, {"last_name": last_name})
            elif patient_id:
                query_1 = text('SELECT * FROM patient_info WHERE patient_id = :patient_id')
                result_1 = connection.execute(query_1, {"patient_id": patient_id})
            elif date_of_birth:
                query_1 = text('SELECT * FROM patient_info WHERE date_of_birth = :date_of_birth')
                result_1 = connection.execute(query_1, {"date_of_birth": date_of_birth})
            else:
                query_1 = text('SELECT * FROM patient_info')
                result_1 = connection.execute(query_1)   
            table_1 = result_1.fetchall()

        return render_template('patients.html', data1=table_1, user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)