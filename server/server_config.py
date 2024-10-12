########################
# File serverConfig.py #
########################


# Instructions & Help:
# Server deployment with Python: From A to Z.
# https://www.codementor.io/@pietrograndinetti/server-deployment-with-python-from-a-to-z-1fjhy96qni
# https://gist.github.com/006f8f4709ac963a9960819f304cd01e.git

# https://friendlyuser.github.io/posts/tech/2023/Using_Fabric_in_Python_A_Step-by-Step_Guide/


# This script needs:
# $ pip install fabric


# Python package called fabric is a function that creates a connection to the server:


from fabric import Connection
from os import environ
import secret

def create_conn():
    # Switch the two lines if you connect via PEM Key instead of password.
    params = {
        #'key_filename': environ['SSH_KEY_PATH']
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


def _create_vm(conn):
    _install_packages(conn)
    _create_new_user(conn)


def _install_packages(conn):
    conn.sudo('apt update && apt upgrade -y')
    conn.sudo('apt install unattended-upgrades')
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
    conn.sudo('apt-get install -y snapd')
    conn.sudo('snap install core')
    conn.sudo('snap refresh core')
    conn.sudo('systemctl enable --now snapd.socket')
    conn.sudo('apt-get install -y uuid-dev')
    conn.sudo('apt-get install -y lzma-dev')
    conn.sudo('apt-get install -y wget')
    conn.sudo('apt-get install -y tree')
    conn.sudo('apt-get install -y curl')
    conn.sudo('apt-get install -y vim')
    conn.sudo('apt-get install -y ca-certificates')
    conn.sudo('apt-get install -y lsb-release')
    conn.sudo('apt-get install -y gnupg')
    conn.sudo('apt-get install -y python3-pip')
    conn.sudo('pip install --upgrade pip')
    conn.sudo('apt-get install -y python3-dev')
    conn.sudo('apt-get install -y python3-setuptools')
    conn.sudo('pip install python-dotenv')
    conn.sudo('apt-get install -y git')
    conn.sudo('apt-get install -y postgresql')
    

def _create_new_user(conn):
    conn.sudo('adduser senior-user')
    conn.sudo('gpasswd -a senior-user sudo')
    # conn.su('- senior-user')
    conn.sudo('mkdir /home/senior-user/.ssh/')
    conn.sudo('chmod 700 -R /home/senior-user/.ssh/')


#####################################
# Functions used from the __main__ ##
#####################################


def create_vm(**kwargs):
    _create_vm(create_conn())


def create_new_user(**kwargs):
    _create_new_user(create_conn())


def main(tasks):
    if len(tasks) <= 1:
        print('No task name found')
        return
    i = 1
    while i < len(tasks):
        try:
            fn = getattr(sys.modules[__name__], tasks[i])
        except AttributeError:
            print(f'Cannot find task {tasks[i]}. Quit.')
            return
        params = {}
        j = i + 1
        while j < len(tasks) and '=' in tasks[j]:
            k, v = tasks[j].split('=')
            params[k] = v
            j += 1
        i = j
        print(f'Function is {fn}')
        print(f'args are {params}')
        fn(**params)


if __name__ == '__main__':
    '''
    Run it with
    $ python main <task1> <key1-task1>=<value1-task1> <key2-task1>=<value2-task2> <task2> <key1-task2>=<value1-task2>
    E.g.
    $ python main create_vm
    
    Or
    $ python main pull_repo branch=develop
    '''
    import sys
    tasks = sys.argv
    main(tasks)