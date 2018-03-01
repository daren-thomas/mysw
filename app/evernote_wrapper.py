"""
Wrap access to Evernote.
"""

import os

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec


class EvernoteWrapper(object):
    """A wrapper class around the EvernoteClient and friends"""

    @staticmethod
    def get_dev_token():
        """FIXME: When done with development, figure out the proper way to get Evernote access."""
        return open(os.path.expanduser('~/evernote.devtoken'), 'r').read().rstrip()

    def __init__(self):
        self.client = EvernoteClient(token=self.get_dev_token(), sandbox=False)
        user_store = self.client.get_user_store()
        self.user = user_store.getUser()

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
        note_filter.tagGuids = [self.tags[tn].guid for tn in tag_names if tn]
        result_spec = NotesMetadataResultSpec()
        result_spec.includeTitle = True
        result_spec.includeTagGuids = True
        notes = self.note_store.findNotesMetadata(note_filter, 0, 100, result_spec)
        for note in notes.notes:
            yield note

    def next_actions(self, level='1-Now', context='all'):
        """return a list of NextAction objects"""
        context = '@' + context

        if not context in self.tags.keys():
            context = None

        assert level in self.tags.keys(), 'Unknown level tag: %s' % level
        assert len(level.split('-')) == 2, 'Not a level tag: %s' % level
        # FIXME: maybe do some more checking here...

        return [NextAction(note) for note in self.get_notes(level, context)]


class NextAction(object):
    def __init__(self, note):
        self.guid = note.guid
        self.title = note.title.decode('utf-8')
        self.note = note


if __name__ == '__main__':
    # take this for a bit of a spin
    evernote = EvernoteWrapper()
    for na in evernote.next_actions():
        print("%s - %s" % (na.guid, na.title))