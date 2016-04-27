from evernote.api.client import EvernoteClient

dev_token = open('devtoken', 'r').read().rstrip()
print dev_token
client = EvernoteClient(token=dev_token)
userStore = client.get_user_store()
user = userStore.getUser()
print user.username

note_store = client.get_note_store()
notebooks = note_store.listNotebooks()
for n in notebooks:
    print n.name