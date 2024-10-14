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
    _secure_server(conn)
    _install_software_tools(conn)
    # _clone_repo(conn)
    # _create_vitual_env(conn)
    # _configure_gunicorn(conn)
    # _configure_supervisor(conn)
    # _configure_nginx(conn)
    # _ssl_certificate_cerbot(conn)


def _secure_server(conn):
    # Set up your server so that you connect to it using an SSH key instead of a password.
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('sudo rm -r ~/.ssh')
        conn.run('sudo mkdir ~/.ssh/')
        conn.run('sudo chmod 700 -R ~/.ssh/')
        conn.run('sudo echo >> ~/.ssh/authorized_keys')  # new line
        conn.run(f'sudo echo {secret_user.Public_SSH_key} >> ~/.ssh/authorized_keys')
        
        # Disable the root login and password authentication rather than an SSH key for SSH connections.
        conn.run('sudo sed -i \'s|#PermitRootLogin yes|PermitRootLogin no|\' /etc/ssh/sshd_config')
        conn.run('sudo sed -i \'s|#PasswordAuthentication yes|PasswordAuthentication no|\' /etc/ssh/sshd_config')


def _install_software_tools(conn):
    with conn.cd('/home/one-user/ime-ai'):
        
        # Install Python
        conn.run('add-apt-repository ppa:deadsnakes/ppa')
        conn.run('apt update')
        conn.run('apt-get install python3.12 python3.12-venv -y')
        
        # Install Resetter
        # conn.run('add-apt-repository ppa:resetter/ppa')
        # conn.run('apt update')
        # conn.run('apt install resetter')

        # Install Supervisor and NGINX
        conn.run('apt-get install supervisor nginx -y')
        conn.run('systemctl enable supervisor')
        conn.run('systemctl start supervisor')
        
        # Install JS
        # conn.sudo('apt-get install -y npm')
        # conn.sudo('npm i ollama')
    
        # Install Docker:
        # conn.sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg')
        # conn.sudo('echo \
        # "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
        # $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null')
        # conn.sudo('apt-get install -y docker-ce docker-ce-cli containerd.io')


def _clone_repo(conn):
    with conn.cd('/home/one-user'):
        conn.run('git clone https://github.com/Ramin-Hashemi/ime-ai.git')


def _create_vitual_env(conn):
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('python3.12 -m venv .venv')
        conn.run('source .venv/bin/activate')
        conn.run('pip install -r requirements.txt')


def _configure_gunicorn(conn):
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('chmod u+x gunicorn_start')
        conn.run('mkdir run')


def _configure_supervisor(conn):
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('mkdir logs')
        conn.run('sudo touch /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo "[program:fastapi-app]" >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo "command=/home/one-user/ime-ai/gunicorn_start" >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo "user=one-user" >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo "autostart=true" >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo "autorestart=true" >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo "redirect_stderr=true" >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('sudo echo "stdout_logfile=/home/one-user/ime-ai/logs/gunicorn-error.log" >> /etc/supervisor/conf.d/fastapi-app.conf')
        conn.run('supervisorctl reread')
        conn.run('supervisorctl update')
        conn.run('supervisorctl restart fastapi-app')


def _configure_nginx(conn):
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/')
        conn.run('usermod -aG main-user www-data')
        conn.run('nginx -t')
        conn.run('systemctl restart nginx')


def _ssl_certificate_cerbot(conn):
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('snap install --classic certbot')
        conn.run('ln -s /snap/bin/certbot /usr/bin/certbot')
        conn.run('certbot --nginx')


#####################################
# Functions used from the __main__ ##
#####################################


def create_app(**kwargs):
    _create_app(create_conn())


def secure_server(**kwargs):
    _secure_server(create_conn())


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