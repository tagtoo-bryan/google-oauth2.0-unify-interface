import json
import flask
import httplib2
from apiclient import discovery
from oauth2client import client

import os
from flask import send_from_directory

app = flask.Flask(__name__)

@app.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        drive_service = discovery.build('drive', 'v2', http_auth)
        files = drive_service.files().list().execute()
        return json.dumps(files)


@app.route('/oauth2callback')
def oauth2callback():

    flow = client.OAuth2WebServerFlow(
        client_id='777124909504-eb9r5bgc5csgi8avs2299dg0h0pfk9he.apps.googleusercontent.com',
        client_secret='O61HOy3yoq9xCPEst3UBG6vq',
        scope='https://www.googleapis.com/auth/drive.metadata.readonly',
        redirect_uri=flask.url_for('oauth2callback', _external=True),)
    #include_granted_scopes=True)

    '''
    flow = client.flow_from_clientsecrets(
        'client_secret.json',
        scope='https://www.googleapis.com/auth/drive.metadata.readonly',
        redirect_uri=flask.url_for('oauth2callback', _external=True),)
    #include_granted_scopes=True)
    '''


    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()



