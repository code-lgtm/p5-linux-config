import random, string, json, os, httplib2, requests
from . import auth
from flask import render_template, flash,make_response, request, redirect
from flask import session as login_session
from flask.ext.login import current_user, login_user
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from ..model import User, Category


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Entry to the application. Renders Login Page

    :return:
    A randomized state token that needs to be passed by clients in subsequent requests to
    prevent cross site request forgery.

    Redirects to dashboard page if user is already logged in
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    print current_user
    return render_template('auth/login.html', STATE=state)

@auth.route('/submit', methods=['POST'])
def submit():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    email = request.form['email']
    user = User.query.filter_by(email=email).first()

    if user is not None and user.verify_password(request.form['password']):
        login_user(user)
        categories = Category.query.all()
        return render_template('main/dashboard.html', categories=categories)

    flash('Invalid username or password')
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('auth/login.html', STATE=state)


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
    2) 500 - If access token is invalid
    3) 500 - Communication with facebook servers fails
    4) 200 - If login succeeds
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for long-lived server side token
    cur_file_path = os.path.dirname(__file__)
    fb_filename = os.path.join(cur_file_path, 'secrets/fb_client_secrets.json')
    app_id = json.loads(open(fb_filename, 'r').read())['web']['app_id']
    app_secret = json.loads(open(fb_filename, 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type' \
          '=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    print url
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
    user_id = get_userid()
    if not user_id:
        user_id = create_social_user(login_session['email'], login_session['username'],' ')
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'

    output += '<img src="'
    output += login_session['picture']
    output += '" style="width: 300px; height: 300px;">'

    flash("You are now logged in as %s" % login_session['username'])

    return output

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
    2) 401 - Failed to upgarde the authorization code - If credentials object cannot be created using the client
             secrets json file
    3) 500 - Error - If access token is invalid
    4) 401 - Token's user Id does not match given userId
    5) 401 - Token's Client ID does not match app's
    6) 200 - Success - Returning user
    7) 200 - Success - New session
    """
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid State Token'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        global filename
        o_auth_flow = flow_from_clientsecrets(filename,
                                              scope='')
        o_auth_flow.redirect_uri = 'postmessage'
        credentials = o_auth_flow.step2_exchange(code)
    except FlowExchangeError as excep:
        response = make_response(json.dumps('Failed to upgarde the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as excep:
        print excep

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps('error'), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user Id does not match given userId"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's Client ID does not match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and stored_gplus_id == gplus_id:
        response = make_response(json.dumps("User already logged in"), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    print data

    login_session['username'] = data['given_name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['family_name'] = data['family_name']

    # response = make_response(json.dumps("Successful"), 200)
    # response.headers['Content-Type'] = 'application/json'

    # see if a user exists, if it doesn't make a new one
    user_id = get_userid()
    if not user_id:
        user_id = create_social_user(data['email'], data['given_name'],
                              data['family_name'])
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'

    output += '<img src="'
    output += login_session['picture']
    output += '" style="width: 300px; height: 300px;">'

    flash("You are now logged in as %s" % login_session['username'])

    return output

@auth.route('/fbdisconnect')
def fbdisconnect():
    """ Disconnects a logged in user

    :return:
    One of the following responses:
    One of following responses:
    401 - Current user not connected
    200 - Successfully disconnected
    400 - Failed to revoke access for logged in user
    """
    facebook_id = login_session['facebook_id']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['facebook_id']

    return "you have been logged out"

@auth.route('/gdisconnect')
def gdisconnect():
    """ Disconnects a logged in user

    :return:
    One of following responses:
    401 - Current user not connected
    200 - Successfully disconnected
    400 - Failed to revoke access for logged in user
    """
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token
    access_token = credentials.access_token
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset's the user session
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps("Successfully disconnected"), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps('Failed to revoke token for the given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

def get_name():
    return 'authentication server'