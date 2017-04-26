from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
import facebook as fb
from flask import Blueprint
from apps import app

app_oauth = Blueprint('app_oauth', __name__,template_folder='templates')

###https://github.com/mitsuhiko/flask-oauth/tree/master/example
SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = '236507713421072'
FACEBOOK_APP_SECRET = '75cb7fb97ea05ea1f27f14e0fd5605df'

method = None
#app = Flask(__name__)
#app.debug = DEBUG
#app.secret_key = SECRET_KEY
oauth = OAuth()




facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email,user_birthday'}
    #request_token_params={'scope': 'email,user_birthday,user_photos,publish_actions,user_friends,user_relationships,user_status'}
)

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key='503619580307-c2idr2bfvuqvg42kd4477eegff04t2sm.apps.googleusercontent.com',
                          consumer_secret='FBRYxnoR6hR6AsmRta-h49G0')



def get_method():
    global method
    return method

def set_method(m):
    global method
    method = m

def get_user_info(method):
    if method == 'google':
        return get_google_user_info()
    if method == 'facebook':
        return get_facebook_user_info()

    return {}


def get_google_user_info():
    #return {'email': 'prueba'}
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('app_oauth.login_google'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect('/')
        return res.read()
    for l in [item.split('":') for item in res.read().replace('{', '').replace('}','').split(',')]:
        k = l[0].replace('"', '').strip()
        if k == 'id':
            g_id = l[1].replace('"', '').strip()
        elif k == 'name':
            g_name = l[1].replace('"', '').strip()
        elif k == 'email':
            g_email = l[1].replace('"', '').strip()


        #user[k] = v
    return {'id': g_id, 'name': g_name, 'email': g_email}


def get_facebook_user_info():
    graph = fb.GraphAPI(session['oauth_token'][0])
    #me = facebook.get('/me')
    me = graph.get_object("me?fields=email,first_name,last_name,name,birthday")
    return me



@app_oauth.route('/login/facebook')
def login_facebook():
    global method
    method = 'facebook'
    return facebook.authorize(callback=url_for('app_oauth.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@app_oauth.route('/facebook_authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    global method
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    method = 'facebook'
    return redirect('/')




@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')




@app_oauth.route('/login/google')
def login_google():
    global method
    method = 'google'
    callback=url_for('app_oauth.authorized', _external=True)
    return google.authorize(callback=callback)



@app_oauth.route('/authorized/google')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect('/')


@google.tokengetter
def get_access_token():
    return session.get('access_token')
