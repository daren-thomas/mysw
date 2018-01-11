"""
A collection of library function and classes for dealing with Evernote
"""

import os

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


def get_dev_token():
    return open(os.path.expanduser('~/evernote.devtoken'), 'r').read().rstrip()


class Evernote(object):
    """A wrapper class around the EvernoteClient and friends"""

    def __init__(self):
        self.client = EvernoteClient(token=get_dev_token(), sandbox=False)
        userStore = self.client.get_user_store()
        self.user = userStore.getUser()

        self.note_store = self.client.get_note_store()

        # find "Action-Pending" notebook
        notebooks = self.note_store.listNotebooks()
        self.action_pending = [n for n in notebooks if n.name == "Action-Pending"][0]

        # collect all tags
        self.tags = {t.name: t for t in self.note_store.listTags()}
        self.tag_names = {t.guid: t.name for t in self.note_store.listTags()}

    @property
    def context_tag_names(self):
        return sorted([key for key in self.tags.keys() if key.startswith('@')])

    def get_notes(self, *tag_names):
        """Return a list of notes matching the tag_names"""
        note_filter = NoteFilter()
        note_filter.tagGuids = [self.tags[tn].guid for tn in tag_names]
        result_spec = NotesMetadataResultSpec()
        result_spec.includeTitle = True
        result_spec.includeTagGuids = True
        notes = self.note_store.findNotesMetadata(note_filter, 0, 100, result_spec)
        for note in notes.notes:
            yield note