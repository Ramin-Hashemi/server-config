#########################
# File serverConfig2.py #
##################@######


# Instructions & Help:
# Server deployment with Python: From A to Z.
# https://dylancastillo.co/posts/fastapi-nginx-gunicorn.html


from fabric import Connection
from os import environ, path
import serverConfig.secret as secret


def create_conn3():
    # Switch the two lines if you connect via PEM Key instead of password.
    params = {
        'key_filename': environ['SSH_KEY_PATH']
        # 'password': environ['REMOTE_PASSWORD']
    }
    conn = Connection(
        host=environ['REMOTE_HOST'],
        user=environ['REMOTE_USER2'],
        connect_kwargs=params,
    )
    return conn


######################
# Internal Functions #
######################

# The code below disable the root login and use password authentication for SSH connections in server:

# 1- Update the following values in /etc/ssh/sshd_config using vim using sudo privileges:
#    Opens 'sshd_config' with an editor,
#    Paste following values into 'sshd_config',
#       PermitRootLogin no # change to no
#       ...
#       PasswordAuthentication no # change to no
#    Save the changes and close the editor.


def _configUser_ssh(conn):
    _projectAdmin_ssh(conn)    


def _projectAdmin_ssh(conn):
    conn.sudo('su - projectAdmin-user')
    conn.sudo('vim ~/.ssh/sshd_config')
    conn.sudo('add-apt-repository ppa:deadsnakes/ppa')
    conn.sudo('apt-get update')
    conn.sudo('apt-get install python3.12 python3.12-venv -y')
    conn.sudo('apt-get install supervisor nginx -y')
    conn.sudo('systemctl enable supervisor')
    conn.sudo('systemctl start supervisor')
    conn.sudo('snap install ollama')
    conn.sudo('pip install ollama-haystack')
    # conn.sudo('curl -fsSL https://ollama.com/install.sh | sh')
    # conn.sudo('pip install ollama')
    
    # conn.sudo('apt-get install -y npm')
    # conn.sudo('npm i ollama')
    # Install Docker:
    # conn.sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg')
    # conn.sudo('echo \
    # "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    # $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
    # conn.sudo('apt-get install -y docker-ce docker-ce-cli containerd.io')


#####################################
# Functions used from the __main__ ##
#####################################

# The motivation is that sometimes I will want to run one of the functions we saw, and just one.
# And some times they may need arguments in input (this is the case for _pull_repo).

# This means that I want to have a __main__ entrypoint that only runs a function that I want to run in that specific moment,
# and it also passes to it any argument that is coming from command line.

def configUser_ssh(**kwargs):
    _configUser_ssh(create_conn3())


def projectAdmin_ssh(**kwargs):
    _projectAdmin_ssh(create_conn3())
    

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