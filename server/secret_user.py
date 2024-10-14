##################
# File secret.py #
##################


# In the main file, I simply do import secret and all environment variables are loaded.
# The two files main.py and secret.py must be in the same directory.


from os import environ, path


### Connection
environ['REMOTE_HOST'] = '89.32.250.198'
environ['REMOTE_USER'] = 'one-user'
environ['REMOTE_PASSWORD'] = ''
environ['SSH_KEY_PATH'] = '~/.ssh/'
Public_SSH_key = 'SHA256:NwY7+gysPDye3205STS/bo5WmjT5Rez5AbjXRmjOjHo ramin.hashemi.myself@gmail.com'

### Git
environ['GIT_DIR'] = '~/ime-ai'
environ['GIT_DEFAULT_BRANCH'] = 'master'
environ['REPO_URL'] = 'https://github.com/Ramin-Hashemi/ime-ai.git'