import traceback
from functools import wraps
import hashlib
import time

from authlib.integrations.flask_client import OAuth, OAuthError
from flask import *

from . import app

oauth = OAuth(app)

# https://flask-oauthlib.readthedocs.io/en/latest/client.html#facebook-oauth
facebook = oauth.register('facebook',
    # request_token_url=None,
    client_id=app.config['FACEBOOK_APP_ID'],
    client_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'},
    access_token_params={'scope': 'email'},

    api_base_url= 'https://graph.facebook.com/v7.0/',
    access_token_url= 'https://graph.facebook.com/v7.0/oauth/access_token',
    authorize_url= 'https://www.facebook.com/v7.0/dialog/oauth',
    client_kwargs= {'scope': 'email public_profile'},
    # userinfo_endpoint= USERINFO_ENDPOINT,

)
facebook = oauth.create_client('facebook')

@app.context_processor
def context():
    logged_in = False
    try:
        logged_in = 'me' in session or g.user
    except:
        pass

    return dict(logged_in=logged_in, timestamp=time.time())

'''
# https://flask-oauthlib.readthedocs.io/en/latest/client.html#signing-in-authorizing
@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')
'''

@app.route('/login')
def login():
    try:
        scheme = app.config['PREFERRED_URL_SCHEME'] or 'http'
    except:
        print("Error determining URL scheme")
        scheme = "http"
        traceback.print_exc()
    print("URL scheme is {}".format(scheme))
    callback_url = url_for(
        'oauth_authorized',
        next=request.args.get('next') or request.referrer or None,
        _scheme=scheme,
        _external=True
    )
    return facebook.authorize_redirect(callback_url)

@app.route('/logout')
def logout():
    if 'user' in g:
        del g.user
    if 'me' in session:
        del session['me']
    return redirect('/')


@app.route('/oauth-authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')
    resp = facebook.authorize_access_token()

    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(next_url)

    if isinstance(resp, OAuthError):
        return 'Access denied: %s' % resp.message

    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me/?fields=email,name,id,picture.height(50).width(50),first_name,last_name')

    user = me.json()
    email = user['email'].strip().lower()

    if email not in app.config['ALLOWED_USERS']:
        flash("You are not one of the allowed users.  Please ask an admin for access.")
        return logout()

    g.user = user
    session['me'] = user
    try:
        session['picture_url'] = user['picture']['data']['url']
    except KeyError:
        session['picture_url'] = "https://www.gravatar.com/avatar/{}".format(hashlib.md5(email).hexdigest())

    print('Logged in as id={} name={} redirect={}'.format(
        user['id'], user['name'], request.args.get('next')))
    flash('You were signed in as {} ({})'.format(user['name'], user['id']))
    return redirect(next_url)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Checking for a login...")
        user = g.setdefault('user')
        if user is None:
            if 'me' in session and session['me']:
                # Legacy login, TODO remove
                g.user = session['me']
            else:
                print("No login.")
                return redirect(url_for('login', next=request.url))

        email = session['me']['email'].strip().lower()
        if email not in app.config['ALLOWED_USERS']:
            flash("You are not one of the allowed users.  Please ask an admin for access.")
            return logout()

        print("Login OK")
        return f(*args, **kwargs)
    return decorated_function
