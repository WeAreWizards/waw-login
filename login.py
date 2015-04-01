#!/usr/bin/env python

import os
import flask
import jwt
import bcrypt
import json

app = flask.Flask(__name__)

class CONFIG:
    JWT_SECRET = os.environ['WAW_LOGIN_JWT_SECRET']
    DATABASE = []


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = flask.request.args.get('next', '/')

    if ok():
        return flask.redirect(next_url)

    resp = flask.make_response("""
    <html><body>
    <form method="POST" action="">
    <input type="text" name="email" placeholder="email">
    <input type="password" name="password" placeholder="password">
    <button type="submit">login</button></form>
    </body></html>
    """)
    if flask.request.method == 'POST':
        entry = [x for x in CONFIG.DATABASE if x['email'] == flask.request.form['email']]
        if not entry:
            return flask.abort(403)

        user = entry[0]

        hashed = bcrypt.hashpw(
            flask.request.form['password'].encode('utf8'),
            user['bcrypt_password'].encode('utf8')
        )
        if hashed != user['bcrypt_password'].encode('utf8'):
            return flask.abort(403)

        redir = flask.redirect(next_url)
        jwt_cookie = jwt.encode(
            {'user': user['email']},
            CONFIG.JWT_SECRET, algorithm='HS256')
        redir.set_cookie('waw-login', jwt_cookie)
        return redir

    return resp


def ok():
    "Return True if the cookie checks out"
    jwt_cookie = flask.request.cookies.get('waw-login', '')
    try:
        jwt.decode(jwt_cookie, CONFIG.JWT_SECRET, algorithms=['HS256'])
        return True
    except jwt.DecodeError:
        return False


@app.route('/check-jwt-auth')
def check_jwt_auth():
    if ok():
        return ''
    return flask.abort(403)


if __name__ == '__main__':

    with open(os.environ['WAW_LOGIN_DATABASE_PATH']) as f:
        CONFIG.DATABASE = json.load(f)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    port = int(os.environ.get('WAW_LOGIN_PORT', 8005))
    app.run(port=port)
