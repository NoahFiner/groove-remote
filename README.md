# Update.ID Remote GitHub Server
Who needs an actual server when you have GitHub?

## Installation
Clone this repo
Boot up the virtual env
```bash
source .env/bin/activate
```
Make sure you have push access to this repository.

## Usage
1) Make any changes you want to updater.py
2) Run ```python3 generate_update.py``` and follow the on-screen instructions.
3) generate_update.py will generate an MD5 hash of all the files in the current directory, update the version and release notes, and automatically git add/commit/push to this repository.

## Improvements
Make this a server.