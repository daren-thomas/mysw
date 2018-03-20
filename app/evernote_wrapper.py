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

        return [NextAction(note, self.user, level) for note in self.get_notes(level, context)]

    def replace_tag(self, note_guid, old_tag, new_tag):
        """Update a note by replacing the old tag with the new tag"""
        note = self.note_store.getNote(note_guid, True, True, True, True)
        old_tag = self.tags[old_tag]
        new_tag = self.tags[new_tag]
        note.tagGuids = list((set(note.tagGuids) | {new_tag.guid}) - {old_tag.guid})
        self.note_store.updateNote(note)
        print(note.title)


class NextAction(object):
    levels = ['0-Done', '1-Now', '2-Next', '3-Soon', '4-Later', '5-Someday', '6-Waiting']
    state_transitions = {
        '0-Done': ['1-Now'],
        '1-Now': ['0-Done', '2-Next', '6-Waiting'],
        '2-Next': ['1-Now', '3-Soon'],
        '3-Soon': ['4-Later', '2-Next'],
        '4-Later': ['5-Someday', '3-Soon'],
        '5-Someday': ['1-Now'],
        '6-Waiting': ['0-Done', '1-Now']
    }

    def __init__(self, note, user, level):
        self.guid = note.guid
        self.title = note.title.decode('utf-8')
        self.note = note
        self.link = 'evernote:////view/{userid}/{shardid}/{guid}/{guid}'.format(userid=user.id, shardid=user.shardId,
                                                                                guid=note.guid)
        self.level = level
        self.transitions = self.state_transitions[self.level]




if __name__ == '__main__':
    # take this for a bit of a spin
    evernote = EvernoteWrapper()
    for na in evernote.next_actions():
        print("%s - %s" % (na.guid, na.title))
