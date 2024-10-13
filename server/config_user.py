#########################
# File serverConfig2.py #
##################@######


# Instructions & Help:
# How to Securely Deploy a FastAPI app with NGINX and Gunicorn.
# https://dylancastillo.co/posts/fastapi-nginx-gunicorn.html


from fabric import Connection
from os import environ, path
import secret_user


def create_conn():
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


def _create_app(conn):
    _update_ssh(conn)
    _install_software_tools(conn)
    # _clone_repo(conn)
    # _create_vitual_env(conn)
    # _configure_gunicorn(conn)
    # _configure_supervisor(conn)
    # _configure_nginx(conn)
    # _ssl_certificate_cerbot(conn)


def _update_ssh(conn):
    conn.sudo('rm -r ~/.ssh')
    conn.sudo('mkdir ~/.ssh/')
    conn.sudo('chmod 700 -R ~/.ssh/')


def _install_software_tools(conn):
    conn.sudo('add-apt-repository ppa:deadsnakes/ppa')
    conn.sudo('apt update')
    conn.sudo('apt-get install python3.12 python3.12-venv -y')
    # conn.sudo('add-apt-repository ppa:resetter/ppa')
    # conn.sudo('apt update')
    # conn.sudo('apt install resetter')
    conn.sudo('apt-get install supervisor nginx -y')
    conn.sudo('systemctl enable supervisor')
    conn.sudo('systemctl start supervisor')

    # conn.sudo('apt-get install -y npm')
    # conn.sudo('npm i ollama')
    
    # Install Docker:
    # conn.sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg')
    # conn.sudo('echo \
    # "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    # $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
    # conn.sudo('apt-get install -y docker-ce docker-ce-cli containerd.io')


def _clone_repo(conn):
    conn.sudo('git clone https://github.com/Ramin-Hashemi/ime-ai.git')


def _create_vitual_env(conn):
    conn.sudo('cd /home/one-user/ime-ai')
    conn.sudo('python3.12 -m venv .venv')
    conn.sudo('source .venv/bin/activate')
    conn.sudo('pip install -r requirements.txt')


def _configure_gunicorn(conn):
    conn.sudo('chmod u+x gunicorn_start')


def _configure_supervisor(conn):
    conn.sudo('supervisorctl reread')
    conn.sudo('supervisorctl update')
    conn.sudo('supervisorctl restart fastapi-app')


def _configure_nginx(conn):
    conn.sudo('ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/')
    conn.sudo('usermod -aG main-user www-data')
    conn.sudo('nginx -t')
    conn.sudo('systemctl restart nginx')


def _ssl_certificate_cerbot(conn):
    conn.sudo('snap install --classic certbot')
    conn.sudo('ln -s /snap/bin/certbot /usr/bin/certbot')
    conn.sudo('certbot --nginx')


#####################################
# Functions used from the __main__ ##
#####################################


def create_app(**kwargs):
    _create_app(create_conn())


def update_ssh(**kwargs):
    _update_ssh(create_conn())


def install_software_tools(**kwargs):
    _install_software_tools(create_conn())


def clone_repo(**kwargs):
    _clone_repo(create_conn())


def create_vitual_env(**kwargs):
    _create_vitual_env(create_conn())


def configure_gunicorn(**kwargs):
    _configure_gunicorn(create_conn())


def configure_supervisor(**kwargs):
    _configure_supervisor(create_conn())


def configure_nginx(**kwargs):
    _configure_nginx(create_conn())


def ssl_certificate_cerbot(**kwargs):
    _ssl_certificate_cerbot(create_conn())


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