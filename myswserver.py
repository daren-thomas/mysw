"""A web app for mysw"""
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/") # take note of this decorator syntax, it's a common pattern
def hello():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

if __name__ == "__main__":
    app.run()