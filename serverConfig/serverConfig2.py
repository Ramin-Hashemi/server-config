#########################
# File serverConfig2.py #
##################@######


# Instructions & Help:
# Server deployment with Python: From A to Z.
# https://dylancastillo.co/posts/fastapi-nginx-gunicorn.html


from fabric import Connection
from os import environ, path
import serverConfig.secret as secret


def create_conn2():
    # Switch the two lines if you connect via PEM Key instead of password.
    params = {
        # 'key_filename': environ['SSH_KEY_PATH']
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

# The code below implements these sub-steps in server:
# 1- Create a user name fastapi-user,
# 2- Add it to the sudo group (which contains all users with root privileges),
# 3- And then log in as that user.
# 4- Create a .ssh directory
# 5- Set the necessary permissions (the owner of .ssh/ has full read, write, and execute permissions, but other users and groups shouldn’t).
# 6- Opens 'authorized_keys' with an editor,
#    Paste your public SSH key into authorized_keys,
#    Save the changes and close the editor.


def _configUser(conn):
    _projectAdmin_config(conn)    


def _projectAdmin_config(conn):
    conn.sudo('adduser projectAdmin-user')
    conn.sudo('gpasswd -a projectAdmin-user sudo')
    conn.sudo('su - projectAdmin-user')
    conn.sudo('mkdir ~/.ssh/')
    conn.sudo('chmod 700 -R ~/.ssh/')
    conn.sudo('vim ~/.ssh/authorized_keys')


#####################################
# Functions used from the __main__ ##
#####################################

# The motivation is that sometimes I will want to run one of the functions we saw, and just one.
# And some times they may need arguments in input (this is the case for _pull_repo).

# This means that I want to have a __main__ entrypoint that only runs a function that I want to run in that specific moment,
# and it also passes to it any argument that is coming from command line.

def configUser(**kwargs):
    _configUser(create_conn2())


def projectAdmin_config(**kwargs):
    _projectAdmin_config(create_conn2())
    

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