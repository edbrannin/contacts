from functools import wraps
import pprint
import hashlib

from flask_oauthlib.client import OAuth, OAuthException
from flask import *

from . import app
from .model import Contact

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

# https://flask-oauthlib.readthedocs.io/en/latest/client.html#signing-in-authorizing
@facebook.tokengetter
def get_facebook_token(token=None):
    return session.get('oauth_token')


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app.route('/oauth-authorized')
def oauth_authorized():
    next_url = request.args.get('next') or url_for('index')
    resp = facebook.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    pprint.pprint(resp)
    session['oauth_token'] = (resp['access_token'], '')
    pprint.pprint(session)
    me = facebook.get('/me/?fields=email,name,id,picture.height(50).width(50),first_name,last_name')
    g.user = me.data
    try:
        session['picture_url'] = me.data['picture']['data']['url']
    except KeyError:
        email = me.data['email'].ostrip().lower()
        session['picture_url'] = "https://www.gravatar.com/avatar/{}".format(hashlib.md5(email).hexdigest())

    print 'Logged in as id={} name={} redirect={}'.format(
        me.data['id'], me.data['name'], request.args.get('next'))
    flash('You were signed in as {} ({})'.format(me.data['name'], me.data['id']))
    return redirect(next_url)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.setdefault('user')
        if session['me'] and not g.user:
            # Legacy login, TODO remove
            g.user = session['me']
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
