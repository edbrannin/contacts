import traceback
from functools import wraps
import pprint
import hashlib
import time

from flask_oauthlib.client import OAuth, OAuthException
from flask import *

from . import app

oauth = OAuth()

# https://flask-oauthlib.readthedocs.io/en/latest/client.html#facebook-oauth
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=app.config['FACEBOOK_APP_ID'],
    consumer_secret=app.config['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)

@app.context_processor
def context():
    logged_in = False
    try:
        logged_in = 'me' in session or g.user
    except:
        pass

    return dict(logged_in=logged_in, timestamp=time.time())

# https://flask-oauthlib.readthedocs.io/en/latest/client.html#signing-in-authorizing
@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')


@app.route('/login')
def login():
    try:
        scheme = app.config['PREFERRED_URL_SCHEME'] or 'http'
    except:
        print("Error determining URL scheme")
        scheme = "http"
        traceback.print_exc()
    print("URL scheme is {}".format(scheme))
    return facebook.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None,
        _scheme=scheme,
        _external=True))


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
    resp = facebook.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(next_url)

    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    pprint.pprint(resp)
    session['oauth_token'] = (resp['access_token'], '')
    pprint.pprint(session)
    me = facebook.get('/me/?fields=email,name,id,picture.height(50).width(50),first_name,last_name')
    g.user = me.data
    session['me'] = me.data
    email = me.data['email'].strip().lower()

    if email not in app.config['ALLOWED_USERS']:
        flash("You are not one of the allowed users.  Please ask an admin for access.")
        return logout()

    try:
        session['picture_url'] = me.data['picture']['data']['url']
    except KeyError:
        session['picture_url'] = "https://www.gravatar.com/avatar/{}".format(hashlib.md5(email).hexdigest())

    print('Logged in as id={} name={} redirect={}'.format(
        me.data['id'], me.data['name'], request.args.get('next')))
    flash('You were signed in as {} ({})'.format(me.data['name'], me.data['id']))
    return redirect(next_url)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Checking for a login...")
        g.setdefault('user')
        if 'me' in session and session['me'] and not g.user:
            # Legacy login, TODO remove
            g.user = session['me']
        if g.user is None:
            print("No login.")
            return redirect(url_for('login', next=request.url))

        email = session['me']['email'].strip().lower()
        if email not in app.config['ALLOWED_USERS']:
            flash("You are not one of the allowed users.  Please ask an admin for access.")
            return logout()

        print("Login OK")
        return f(*args, **kwargs)
    return decorated_function
