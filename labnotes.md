# Initial setup

- following guide here for using the Evernote SDK for Python: https://dev.evernote.com/doc/start/python.php
- using the git submodule route (because I have never done that before!)

```
Added C:\Users\darthoma\Anaconda and C:\Users\darthoma\Anaconda\Scripts to PATH.

C:\projects
>cd mysw

C:\projects\mysw
>git submodule add git://github.com/evernote/evernote-sdk-python/ evernote
Cloning into 'evernote'...
remote: Counting objects: 393, done.
remote: Total 393 (delta 0), reused 0 (delta 0), pack-reused 393
Receiving objects: 100% (393/393), 425.51 KiB | 369 KiB/s, done.
Resolving deltas: 100% (143/143), done.
warning: LF will be replaced by CRLF in .gitmodules.
The file will have its original line endings in your working directory.

C:\projects\mysw
>git submodule init
Submodule 'evernote' () registered for path 'evernote'

C:\projects\mysw
>git submodule update

C:\projects\mysw
>
```

Testing the SDK:

```
C:\projects\mysw
>python -c "from evernote.api.client import EvernoteClient"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ImportError: No module named evernote.api.client

C:\projects\mysw
>
```

looks like i still have to do the `python setup.py install`:

```
C:\projects\mysw
>cd evernote

C:\projects\mysw\evernote
>python setup.py install
running install

# NOTE: deleting a bunch of stuff because you don't want to keep this forever, duh!

C:\projects\mysw\evernote
>
```

Testing worked:

```
C:\projects\mysw\evernote
>python -c "from evernote.api.client import EvernoteClient"

C:\projects\mysw\evernote
>
```

