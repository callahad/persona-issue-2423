#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, abort, redirect, render_template, request, session
import requests

import json

app = Flask(__name__)
app.secret_key = '\x87\xb6\x1f\x0e|6l\xfbhn\xd9\x9f\xc1\xca\x08-'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():

    if 'assertion' not in request.form:
        abort(400)

    data = {'assertion': request.form['assertion'], 'audience': 'localhost'}
    resp = requests.post('https://verifier.login.persona.org/verify', data=data)
    if resp.ok:
        verification = json.loads(resp.content)

        if verification['status'] == 'okay':
            session.update({'email': verification['email']})

        return redirect('/')

    abort(500)


# Clear the user's session when they POST to /logout on my server
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('email', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
