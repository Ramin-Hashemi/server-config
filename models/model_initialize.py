############################
# File imeModel_initialize #
############################


from fabric import Connection
from os import environ
from server import secret
import ollama


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

def _initializer(conn):
    conn.sudo('git clone https://github.com/Ramin-Hashemi/ime-ai.git')
    conn.sudo('python3.12 -m venv .venv')
    conn.sudo('source .venv/bin/activate')
    conn.sudo('pip install -r requirements.txt')
    conn.sudo('uvicorn main:app')
    # conn.sudo('ollama pull llama3.2')
    # conn.sudo('ollama create iME -f ~/ime-ai/Modelfile')


def initializer(**kwargs):
    _initializer(create_conn())


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