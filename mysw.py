from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

from myswlib import get_dev_token

dev_token = get_dev_token()

client = EvernoteClient(token=dev_token, sandbox=False)
userStore = client.get_user_store()
user = userStore.getUser()

note_store = client.get_note_store()

# find "Action-Pending" notebook
notebooks = note_store.listNotebooks()
action_pending = [n for n in notebooks if n.name == "Action-Pending"][0]

# collect all tags
tags = {t.name: t for t in note_store.listTags()}
tag_names = {t.guid: t.name for t in note_store.listTags()}

for location_tag in sorted([tags[key] for key in tags.keys() if key.startswith('@')]):
    print '#', location_tag.name
    print
    note_filter = NoteFilter()
    note_filter.tagGuids = [location_tag.guid, tags['1-Now'].guid]
    result_spec = NotesMetadataResultSpec()
    result_spec.includeTitle = True
    result_spec.includeTagGuids = True
    notes = note_store.findNotesMetadata(note_filter, 0, 100, result_spec)
    for n in notes.notes:
        print '-', n.title, ' '.join('*%s*' % tag_names[guid]
                                     for guid in n.tagGuids
                                     if not tag_names[guid] in {'1-Now', location_tag.name})
    print