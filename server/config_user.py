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
    _clone_repo(conn)
    _create_vitual_env(conn)
    _configure_gunicorn(conn)
    _configure_supervisor(conn)
    _configure_nginx(conn)
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
        # Make it executable.
        conn.run('chmod u+x gunicorn_start')
        # make a run folder in your project directory for the Unix socket file you defined in the BIND parameter:
        conn.run('mkdir run')


def _configure_supervisor(conn):
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('mkdir logs')
        # create a Supervisor’s configuration file.
        conn.run('sudo sh -c "echo > /etc/supervisor/conf.d/fastapi-app.conf')
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
        # Reread Supervisor’s configuration file and restart the service.
        conn.run('supervisorctl reread')
        conn.run('supervisorctl update')
        conn.run('supervisorctl restart fastapi-app')


def _configure_nginx(conn):
    with conn.cd('/home/one-user/ime-ai'):
        # Create a new NGINX configuration file.
        conn.run('sudo sh -c "echo > /etc/nginx/sites-available/fastapi-app"')
        conn.run('sudo echo "upstream app_server {" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    server unix:/home/fastapi-user/fastapi-nginx-gunicorn/run/gunicorn.sock fail_timeout=0;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "}" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "server {" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    listen 80;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    # add here the ip address of your server" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    # or a domain pointing to that ip (like example.com or www.example.com)" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    server_name XXXX;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    keepalive_timeout 5;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    client_max_body_size 4G;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    access_log /home/fastapi-user/fastapi-nginx-gunicorn/logs/nginx-access.log;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    error_log /home/fastapi-user/fastapi-nginx-gunicorn/logs/nginx-error.log;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    location / {" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "        proxy_set_header Host $http_host;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "        proxy_redirect off;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "        if (!-f $request_filename) {" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "            proxy_pass http://app_server;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "            break;" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "        }" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "    }" >> /etc/nginx/sites-available/fastapi-app')
        conn.run('sudo echo "}" >> /etc/nginx/sites-available/fastapi-app')
        # Enable the configuration of your site by creating a symbolic link from the file in sites-available into sites-enabled.
        conn.run('ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/')
        # If you get a permission error telling you that NGINX cannot access the unix socket, you can add the www-data user.
        conn.run('usermod -aG main-user www-data')
        # Test that the configuration file is OK and restart NGINX.
        conn.run('nginx -t')
        conn.run('systemctl restart nginx')


def _ssl_certificate_cerbot(conn):
    with conn.cd('/home/one-user/ime-ai'):
        conn.run('snap install --classic certbot')
        conn.run('ln -s /snap/bin/certbot /usr/bin/certbot')
        # generate a certificate for your domain.
        conn.run('certbot --nginx')
        # Certbot will automatically handle the renewal of your certificate. To test that it works run the following:
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