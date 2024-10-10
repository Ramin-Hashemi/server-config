# File secret.py

# In the main file, I simply do import secret and all environment variables are loaded.
# The two files main.py and secret.py must be in the same directory.

from os import environ, path

### Connection
environ['REMOTE_HOST'] = '89.32.250.198'
environ['REMOTE_USER'] = 'root'
environ['REMOTE_PASSWORD'] = 'a6l14GyRdm4'
#
## Python venv
# environ['VENV_NAME'] = 'prod-api'
#
### Git
environ['GIT_DIR'] = '~/app'
environ['GIT_DEFAULT_BRANCH'] = 'main'
environ['REPO_URL'] = 'https://github.com/digitalocean/sample-flask.git'