############################
# File imeModel_initialize #
############################


from serverConfig import create_conn
import ollama


######################
# Internal Functions #
######################

# The code below initialize the iME original model in the following steps:
# 1- Download llama3.2v3B model from haystack.
# 2- Create iME model from the original llama3.2 model previously downloaded in the local server.
#    It is used to create a model from a Modelfile.

def _initializer(conn):
    conn.sudo('ollama pull llama3.2')
    conn.sudo('ollama create iME -f ./Modelfile')
    conn.sudo('fastapi dev main.py')


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