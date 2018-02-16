from flask import Flask, Blueprint, render_template, request, jsonify, redirect, make_response, session, url_for
from functools import wraps

from objects.Utilities import Utilities
from objects.UserProfile import UserProfile

from apis import app_api

util = Utilities()
userProfile = UserProfile()


app = Flask(__name__)
app.register_blueprint(app_api)


app.secret_key = '123'

def userSessionToUsername():
    try:
        user = userProfile.getUserProfile(session['username'])
        return user
    except:
        return 'error'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            #if not logged in
            return redirect(url_for('logout', next=request.url))

        elif userSessionToUsername() == 'error':
            #if user class returns error
            return redirect(url_for('logout', next=request.url))

        elif userSessionToUsername() is None:
            #if user class returns None
            return redirect(url_for('logout', next=request.url))

        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/facebookid/<token>')
def loginFacebook(token):
    # if it exists get account and login
    if userProfile.getUserProfile(token):
        #get url path
        username = userProfile.getUserProfile(token)['username']
        print username

        session['logged_in'] = True
        session['username'] = token
        return redirect('/config', code=302)

    # else create account using fb token
    else:
        userProfile.buildUserProfileFromFB(token)
        session['logged_in'] = True
        session['username'] = token
        return redirect('/config?=new-user', code=302)

@app.route('/<username>')
def profile(username):
    userFromDB = userProfile.getUserProfile(username)
    userFromSession = userSessionToUsername()

    #profile not found
    if userFromDB == None:
        return render_template('404.html')

    #tried to access someone else's page
    elif userFromSession == 'error':
        return render_template('profile.html', user=userFromDB, isUser=False)

    #is your own page
    elif userFromDB['username'] == userFromSession['username']:
        return render_template('config.html', user=userFromDB, isUser=True)


@app.route('/config')
@login_required
def configPage():
    return render_template('config.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/", code=302)

if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=5007)
