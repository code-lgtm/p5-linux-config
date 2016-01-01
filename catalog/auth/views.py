"""
Available Authorization views exposed by the server
Following views are available as part of this package
 1) Login
 2) Registration
 3) Google Plus Sign In
 4) Facebook Sign In
"""

import random, string, json, os, httplib2, requests
from . import auth
from flask import render_template, flash, make_response, request, redirect
from flask import session as login_session
from flask.ext.login import current_user, login_user, logout_user
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from flask import url_for, abort
from forms import RegistrationForm, LoginForm
from ..model import User
from catalog import db, csrf

# Extract CLIENT_ID from the secrets file downloaded from Google website
file_path = os.path.dirname(__file__)
filename = os.path.join(file_path, 'secrets/client_secrets.json')
CLIENT_ID = json.loads(open(filename, 'r').read())['web']['client_id']

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Entry to the application. Renders Login Page

    :return:
    A randomized state token that needs to be passed by clients in subsequent requests to
    prevent cross site request forgery.

    Redirects to dashboard page if user is already logged in
    Renders login page id user needs to log-in
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Username or password invalid')

    if current_user.is_authenticated():
        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registrations Form for new users. Creates a new user
    if all validations are cleared

    :return:
    For POST request :Redirects to Login Page if user is successfully created
    For GET request : Renders Registration Page
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/fbconnect', methods=['POST'])
def fbconnect():
    """ Connects with facebook server to authenticate users.
    Checks:
    1) if CSRF token is valid
    2) Checks  the authenticity of the user by verifying access token

    Registers user with the local database if it is not present

    :return:
    One of following responses:
    1) 401 - Invalid State Token - if the state token is invalid
    2) If login succeeds - Redirects to dashboard page
    """
    access_token = request.data

    # Exchange client token for long-lived server side token
    cur_file_path = os.path.dirname(__file__)
    fb_filename = os.path.join(cur_file_path, 'secrets/fb_client_secrets.json')
    app_id = json.loads(open(fb_filename, 'r').read())['web']['app_id']
    app_secret = json.loads(open(fb_filename, 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type' \
          '=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)

    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.2/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.2/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Get User Picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200' \
          '&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads((result))
    login_session['picture'] = data["data"]["url"]

    # see if a user exists, if it doesn't make a new one
    user = User.query.filter_by(email=login_session['email']).first()
    if not user:
        new_user = User(email=login_session['email'], name=login_session['username'])
        login_user(new_user)
        login_session['user_id'] = new_user.id
    else:
        login_user(user)
        login_session['user_id'] = user.id

    return redirect(url_for('main.dashboard'))


@auth.route('/gconnect', methods=['POST'])
def gconnect():
    """ Connects with google API server to authenticate users.
    Checks:
    1) if CSRF token is valid
    2) Checks  the authenticity of the user by verifying google id and client ID
    3) Store session state to validate returning users
    4) Checks if the one time code provided by the client is valid

    :return:
    One of following responses:
    1) 401 - Invalid State Token - if the state token is invalid
    2) 401 - Failed to upgarde the authorization code -
             If credentials object cannot be created using the client
             secrets json file
    3) 500 - Error - If access token is invalid
    4) 401 - Token's user Id does not match given userId
    5) 401 - Token's Client ID does not match app's
    6) Redirect to dashboard is login is successful
    """
    code = request.data

    try:
        global filename
        o_auth_flow = flow_from_clientsecrets(filename,
                                              scope='')
        o_auth_flow.params['access-type'] = 'offline'
        o_auth_flow.redirect_uri = 'postmessage'
        credentials = o_auth_flow.step2_exchange(code)
    except FlowExchangeError as excep:
        abort(401)
    except Exception as excep:
        print excep

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        abort(500)

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        abort(401)

    if result['issued_to'] != CLIENT_ID:
        abort(401)

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and stored_gplus_id == gplus_id:
        return redirect(url_for('main.dashboard'))

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['given_name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['family_name'] = data['family_name']

    # see if a user exists, if it doesn't make a new one
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(email=data['email'], name=data['given_name'])
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        login_session['user_id'] = new_user.id
    else:
        login_session['user_id'] = user.id
        login_user(user)

    return redirect(url_for('main.dashboard'))


@auth.route('/logout')
def logout():
    """
    Logouts a user. Deletes all saved states associated with login of the user

    :return:
    """

    credentials = login_session.get('credentials')
    if credentials is not None:
        # Execute HTTP GET request to revoke current token
        access_token = credentials.access_token
        url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]

        if result['status'] == '200':
            del login_session['credentials']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            del login_session['user_id']
            del login_session['family_name']

    if login_session.get('facebook_id') is not None:
        facebook_id = login_session['facebook_id']
        url = 'https://graph.facebook.com/%s/permissions' % facebook_id
        h = httplib2.Http()
        result = h.request(url, 'DELETE')[1]
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['facebook_id']
    logout_user()
    return redirect(url_for('main.dashboard'))


def get_name():
    return 'authentication server'
