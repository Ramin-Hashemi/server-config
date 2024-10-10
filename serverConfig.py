# File serverConfig.py

# Instructions & Help:
# Server deployment with Python: From A to Z.
# https://www.codementor.io/@pietrograndinetti/server-deployment-with-python-from-a-to-z-1fjhy96qni
# https://gist.github.com/006f8f4709ac963a9960819f304cd01e.git

# https://friendlyuser.github.io/posts/tech/2023/Using_Fabric_in_Python_A_Step-by-Step_Guide/


# This script needs:
# $ pip install fabric


# Create a file `secret.py` in the same directory as this one
# and add in it the credentials to connect to the server and GitHub.


# Python package called fabric is a function that creates a connection to the server:


#  Finally, run these four simple commands:
# The first one took a few minutes (remember that it compiles and install Python),
# and when everything is done, the web app is running in the server!!

# python serverConfig.py create_vm
# python serverConfig.py pull_repo
# python aserverConfig.py install_project
# python serverConfig.py restart_web


from fabric import Connection
from os import environ
import secret

def create_conn():
    # Switch the two lines if you connect via PEM Key instead of password.
    params = {
        #'key_filename': environ['SSH_KEY_PATH']}
        'password': environ['REMOTE_PASSWORD']
    }
    conn = Connection(
        host=environ['REMOTE_HOST'],
        user=environ['REMOTE_USER'],
        connect_kwargs=params,
    )
    return conn

######################
# Internal Functions #
######################

# The code below implements the three sub-steps in server:

# 1- Install all libraries that we need at the OS-level (in this case there are also git and postgresql-server, among many others).
# 2- Install the specific Python version that we want, compiling it from source code.
# 3- Install virtualenvwrapper. In fact, you could use any virtualenv software management, or none if the machine is dedicated to only one Python app.
# If you look carefully at the code, you will understand every task is accomplished by creating a connection object and using its .run() method, with argument the same command you'd run manually.

def _create_vm(conn):
    _install_packages(conn)
    _install_python(conn)
    # _install_venv(conn)
    _pull_repo(conn)


def _install_packages(conn):
    conn.sudo('apt-get -y update')
    conn.sudo('apt-get -y upgrade')
    conn.sudo('apt-get install -y build-essential')
    conn.sudo('apt-get install -y checkinstall')
    conn.sudo('apt-get install -y libreadline-gplv2-dev')
    conn.sudo('apt-get install -y libncurses-dev')
    conn.sudo('apt-get install -y libncursesw5-dev')
    conn.sudo('apt-get install -y libssl-dev')
    conn.sudo('apt-get install -y libsqlite3-dev')
    conn.sudo('apt-get install -y tk-dev')
    conn.sudo('apt-get install -y libgdbm-dev')
    conn.sudo('apt-get install -y libpq-dev')
    conn.sudo('apt-get install -y libc6-dev')
    conn.sudo('apt-get install -y libbz2-dev')
    conn.sudo('apt-get install -y zlib1g-dev')
    conn.sudo('apt-get install -y openssl')
    conn.sudo('apt-get install -y libffi-dev')
    conn.sudo('apt-get install -y python3-dev')
    conn.sudo('apt-get install -y python3-setuptools')
    conn.sudo('apt-get install -y uuid-dev')
    conn.sudo('apt-get install -y lzma-dev')
    conn.sudo('apt-get install -y wget')
    conn.sudo('apt-get install -y curl')
    conn.sudo('apt-get install -y python3-pip')
    conn.sudo('apt-get install -y git')
    conn.sudo('apt-get install -y postgresql')
    conn.sudo('curl -fsSL https://ollama.com/install.sh | sh')
    conn.sudo('pip install -y ollama')
    conn.sudo('npm i -y ollama')
    conn.sudo('pip install -y ollama-haystack')


def _install_python(conn):
    """Install python 3.7 in the remote machine."""

    res = conn.run('python3 --version')
    if '3.7' in res.stdout.strip():
        # Python >= 3.7 already exists
        return

    conn.run('rm -rf /tmp/Python3.7 && mkdir /tmp/Python3.7')

    with conn.cd('/tmp/Python3.7'):
        conn.run('wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz')
        conn.run('tar xvf Python-3.7.0.tar.xz')

    with conn.cd ('/tmp/Python3.7/Python-3.7.0'):
        conn.run('./configure --enable-optimizations')
        conn.run('make')

    # see https://github.com/pyinvoke/invoke/issues/459
    conn.sudo('bash -c "cd /tmp/Python3.7/Python-3.7.0 && make altinstall"')


def _install_venv(conn):
    """Install virtualenv, virtualenvwrapper."""

    res = conn.run('which python3.7')
    res = res.stdout.strip()
    py_path = res

    conn.sudo('apt install -y virtualenvwrapper')

    # for a standard Debian distro
    venv_sh = '/usr/share/virtualenvwrapper/virtualenvwrapper.sh'

    conn.run('echo >> ~/.bashrc')  # new line
    conn.run(f'echo source {venv_sh} >> ~/.bashrc')
    conn.run('echo >> ~/.bashrc')  # new line
    conn.run('echo export LC_ALL=en_US.UTF-8 >> ~/.bashrc')
    conn.run('source ~/.bashrc')
    env = environ['VENV_NAME']
    with conn.prefix(f'source {venv_sh}'):
        conn.run(f'mkvirtualenv -p {py_path} {env}')


# The function is a general function that allows you to checkout a specific branch, by name, or a specific commit, by its hash.

def _pull_repo(conn, branch=None, commit=None):
    if branch and commit:
        raise ValueError('Cannot provide both branch name and commit hash')
    source = environ['GIT_DIR']
    if not branch:
        branch = environ['GIT_DEFAULT_BRANCH']
    repo = environ['REPO_URL']
    if commit:
        print('Hash provided. Resetting to that commit.')
        conn.run(
            f"cd {source} && "
            'git stash && '
            f'git reset --hard {commit} && '
            'git checkout -B tmp_branch'
        )
    else:
        if conn.run(f'test -e {source}/.git', warn=True).ok:
            print('Repo already exists.')
        else:
            print('Repo did not exist. Creating it...')
            conn.run(f'git clone {repo} {source}')
            conn.run(f'cd {source} && git remote set-url origin {repo}')
        print('Checking out the requested branch...')
        conn.run(f'cd {source} && git fetch origin && git checkout {branch} && git pull origin {branch}')
    current_hash = conn.run(f'cd {source} && git log -n 1 --format=%H', hide='both')
    current_hash = current_hash.stdout.strip()
    print(f'Checked out {current_hash}')
    return current_hash



# This function is to install the Python requirements. The only trick here is that I use conn.cd() and conn.prefix() to activate the virtualenv before installing the requirements.
# Other than that, the main command is exactly like you would run manually: pip install -r requirements.txt

def _install_project(conn):
    repo_path = environ['GIT_DIR']
    venv_name = environ['VENV_NAME']
    venv_sh = 'source /usr/share/virtualenvwrapper/virtualenvwrapper.sh'
    with conn.cd(repo_path):
        with conn.prefix(
            f'{venv_sh} && workon {venv_name}'
        ):
            conn.run('pip install --upgrade pip')
            conn.run('pip install -r requirements.txt')
            # # If your project as a `setup.py` then install project.
            # conn.run('pip install -e .')


# I use Gunicorn as production web server, and to run it you just need to run a simple line:
# gunicorn <app_module_path>

# I do a few more things in the code:

# First, I stop the process gunicorn if it's already running. This will cause a bit of downtime in the app.
# Then I use some configuration arguments to the new gunicorn process to make sure it runs correctly:
# -b it binds it to the port I want (8080 in this example);
# -w specifies the number of workers (processes);
# --daemon runs it in the background,
# so that you don't have to keep the connection open.

def _restart_web(conn):
    try:
        conn.sudo('pkill gunicorn')
    except:
        pass # may not be running at all.
    repo_path = environ['GIT_DIR']
    venv_name = environ['VENV_NAME']
    venv_sh = 'source /usr/share/virtualenvwrapper/virtualenvwrapper.sh'
    with conn.cd(repo_path):
        with conn.prefix(
            f'{venv_sh} && workon {venv_name}'
        ):
            conn.run("gunicorn app:app -b 0.0.0.0:8080 -w 3 --daemon")


#####################################
# Functions used from the __main__ ##
#####################################

# The motivation is that sometimes I will want to run one of the functions we saw, and just one.
# And some times they may need arguments in input (this is the case for _pull_repo).

# This means that I want to have a __main__ entrypoint that only runs a function that I want to run in that specific moment,
# and it also passes to it any argument that is coming from command line.

def create_vm(**kwargs):
    _create_vm(create_conn())


# def pull_repo(**kwargs):
#     conn = create_conn()
#     _pull_repo(conn, **kwargs)


# def install_project(**kwargs):
    # _install_project(create_conn())


# def restart_web(**kwargs):
    # _restart_web(create_conn())


# def main(tasks):
#     if len(tasks) <= 1:
#         print('No task name found')
#         return
#     i = 1
#     while i < len(tasks):
#         try:
#             fn = getattr(sys.modules[__name__], tasks[i])
#         except AttributeError:
#             print(f'Cannot find task {tasks[i]}. Quit.')
#             return
#         params = {}
#         j = i + 1
#         while j < len(tasks) and '=' in tasks[j]:
#             k, v = tasks[j].split('=')
#             params[k] = v
#             j += 1
#         i = j
#         print(f'Function is {fn}')
#         print(f'args are {params}')
#         fn(**params)


# if __name__ == '__main__':
#     '''
#     Run it with
#     $ python main <task1> <key1-task1>=<value1-task1> <key2-task1>=<value2-task2> <task2> <key1-task2>=<value1-task2>
#     E.g.
#     $ python main create_vm
    
#     Or
#     $ python main pull_repo branch=develop
#     '''
#     import sys
#     tasks = sys.argv
#     main(tasks)