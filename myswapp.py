"""
Provide a graphical user interface (GUI) to the user configuration file (``cea.config``).

This implementation is based on TkInter for maximal portability.
"""
from __future__ import division
from __future__ import print_function

import os
import json
import htmlPy

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import myswlib

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Backend(htmlPy.Object):
    """Contains the backend functions, callable from the GUI."""
    def __init__(self):
        super(Backend, self).__init__()
        # Initialize the class here, if required.
        pass

    @htmlPy.Slot(str, result=str)
    def test(self, name):
        return 'hello ' + name


class NextAction(object):
    def __init__(self, guid, title, context, level):
        self.guid = guid
        self.title = title
        self.context = context
        self.level = level

def next_actions(evernote):
    """return a list of NextAction objects"""
    result = {}
    for context in evernote.context_tag_names:
        result[context] = []
        for note in evernote.get_notes('1-Now', context):
            result[context].append(NextAction(guid=note.guid, title=note.title.decode('utf-8'),
                                              context=context, level='1-Now'))
    return result


def main(evernote):
    """
    Start up the GUI with the list of 1-Now next actions
    """
    app = htmlPy.AppGUI(title=u"MySW - Next Actions", maximized=False, developer_mode=True)

    app.template_path = os.path.join(BASE_DIR, 'templates')
    app.static_path = os.path.join(BASE_DIR, 'static')

    app.template = ("myswapp.html", {"next_actions": next_actions(evernote), "evernote": evernote})
    app.bind(Backend(), variable_name='backend')
    app.start()


if __name__ == '__main__':
    main(evernote = myswlib.Evernote())
