# List of checks

This file contains some consistency checks to make sure TSW is working:

- check that all `tag:1-Now`, `tag:2-Next` (etc.) tags are in `notebook:Action-Pending`
- check that no reminders exist for `notebook:Completed` notes
- move `tag:2-Next` with reminder this week to `tag:1-Now` (do the same for `tag:3-Soon` etc. in the future!)