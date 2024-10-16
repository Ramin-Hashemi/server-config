########################
# File serverConfig.py #
########################


import subprocess
import secret
import sys
import os


def prepare_server():
    install_packages()
    unattended_upgrades()
    create_new_users()
    # secure_server()
    clone_repo()
    create_virtual_env()
    create_django_project()
    # configure_gunicorn()
    # configure_supervisor()
    # configure_nginx()
    # ssl_certificate_certbot()


def install_packages():
    # Recommended for start
    subprocess.run(["sudo", "apt-get", "update", "-y"])
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"])

    # Projects required packages
    subprocess.run(["sudo", "apt-get", "install", "-y", "unattended-upgrades"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "build-essential"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "checkinstall"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "coreutils"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libreadline-gplv2-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libncurses-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libncursesw5-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libssl-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libsqlite3-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "tk-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libgdbm-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libc6-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libbz2-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "zlib1g-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "openssl"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "libffi-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "software-properties-common"])
    subprocess.run(["sudo", "systemctl", "enable", "--now", "snapd.socket"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "uuid-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "lzma-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "wget"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "tree"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "curl"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "vim"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "ca-certificates"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "lsb-release"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "gnupg"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-pip"])
    subprocess.run(["sudo", "pip", "install", "--upgrade", "pip"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-setuptools"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "virtualenv"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "git"])

    # Install Python and its related packages
    subprocess.run(["sudo", "add-apt-repository", "ppa:deadsnakes/ppa", "-y"])
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "python3.11", "-y"])
    subprocess.run(["sudo", "apt-get", "install", "python3.11-venv", "-y"])
    subprocess.run(["sudo", "apt-get", "install", "python-virtualenv", "-y"])

    # Building Python modules
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-dev"])

    # Install PostgreSQL
    subprocess.run(["sudo", "apt-get", "install", "-y", "postgresql"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "postgresql-contrib"])

    # library for communication with Postgres
    subprocess.run(["sudo", "apt-get", "install", "-y", "libpq-dev"])

    # Dependencies
    subprocess.run(["sudo", "pip", "install", "pexpect"])
    subprocess.run(["sudo", "pip", "install", "python-dotenv"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "snapd"])
    subprocess.run(["sudo", "systemctl", "enable", "--now", "snapd.socket"])
    subprocess.run(["sudo", "snap", "install", "core"])
    subprocess.run(["sudo", "snap", "refresh", "core"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "policycoreutils-python-utils"])

    # Install Resetter
    # subprocess.run(["sudo", "add-apt-repository", "ppa:resetter/ppa", "-y"])
    # subprocess.run(["sudo", "apt-get", "update"])
    # subprocess.run(["sudo", "apt-get", "install", "resetter", "-y"])

    # Install Supervisor and NGINX
    subprocess.run(["sudo", "apt-get", "install", "supervisor", "-y"])
    subprocess.run(["sudo", "apt-get", "install", "nginx", "-y"])
    subprocess.run(["sudo", "systemctl", "enable", "supervisor"])
    subprocess.run(["sudo", "systemctl", "start", "supervisor"])

    # Install JS
    subprocess.run(["sudo", "apt-get", "install", "-y", "npm"])

    # Install Ollama
    subprocess.run(["npm", "install", "ollama"])

    # install_docker
    # Add Docker's official GPG key
    subprocess.run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg", shell=True)
    # Set up the stable repository
    subprocess.run('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null', shell=True)
    # Install Docker Engine
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"])


def unattended_upgrades():
    # Configure unattended-upgrades so that it runs automatically.
    subprocess.run('sudo bash -c \'echo "APT::Periodic::Update-Package-Lists \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades\'', shell=True)
    subprocess.run('sudo bash -c \'echo "APT::Periodic::Unattended-Upgrade \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades\'', shell=True)
    subprocess.run('sudo bash -c \'echo "APT::Periodic::AutocleanInterval \\"7\\";" >> /etc/apt/apt.conf.d/20auto-upgrades\'', shell=True)
    # System automatically reboots when kernel updates require it
    subprocess.run('sudo sed -i \'s|//Unattended-Upgrade::Automatic-Reboot "false";|Unattended-Upgrade::Automatic-Reboot "true";|\' /etc/apt/apt.conf.d/50unattended-upgrades', shell=True)


def create_new_users():

    # Create a new system user
    subprocess.run(["sudo", "adduser", "--system", "ramin-hashemi"])
    # Add the new user to the sudo group
    subprocess.run(["sudo", "usermod", "-g", "sudo", "ramin-hashemi"])

    # Create a new user group for ime-app users
    subprocess.run(["sudo", "addgroup", "--system", "ime-users"])
    # Add the ime-app users group to the sudo group
    subprocess.run(["sudo", "gpasswd", "-a", "ime-users", "sudo"])

    # Create a new user for ime-app
    subprocess.run(["sudo", "adduser", "--system", "ime-user-1"])
    # Assign the user to the group
    subprocess.run(["sudo", "usermod", "-g", "ime-users", "ime-user-1"])
    # Set the user’s shell
    subprocess.run(["sudo", "usermod", "--shell", "/bin/bash", "ime-user-1"])
    # Set the user’s home directory
    subprocess.run(["sudo", "usermod", "--home", "/webapps/ime-app", "ime-user-1"])

    # Add the user to the new group (used for secondary membership)
    # subprocess.run(["sudo", "gpasswd", "-a", "ime-user-1", "ime-users"])

    # Create a directory to store your application
    subprocess.run(["sudo", "mkdir", "-p", "/webapps/ime-app"])

    # Allowing other users write access to the application directory
    subprocess.run(["sudo", "chown", "-R", "ime-user-1:users", "/webapps/ime-app"])
    subprocess.run(["sudo", "chmod", "-R", "g+w", "/webapps/ime-app"])
    subprocess.run(["sudo", "usermod", "-a", "-G", "users", "ime-user-1"])


def secure_server():
    # Set up your server so that you connect to it using an SSH key instead of a password.
    os.chdir('/home/webapps')
    subprocess.run(['sudo', 'mkdir', '-p', '/home/webapps/.ssh'])
    subprocess.run(['sudo', 'chmod', '700', '/home/webapps/.ssh'])
    subprocess.run(['sudo', 'chmod', '600', '/home/webapps/.ssh/authorized_keys'])
    subprocess.run(f'sudo bash -c \'echo "{secret.Public_SSH_key}" >> /home/webapps/.ssh/authorized_keys\'', shell=True)

    # Disable the root login and password authentication rather than an SSH key for SSH connections.
    subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PubkeyAuthentication .*|PubkeyAuthentication yes|', '/etc/ssh/sshd_config'])
    # subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PermitRootLogin .*|PermitRootLogin no|', '/etc/ssh/sshd_config'])
    # subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PasswordAuthentication .*|PasswordAuthentication no|', '/etc/ssh/sshd_config'])


def clone_repo():
    os.chdir('/home/ramin-hashemi')
    # Create a directory to store ime-app
    subprocess.run(["sudo", "mkdir", "-p", "web-apps"])
    
    # Clone iME project from GitHub
    os.chdir('/home/ramin-hashemi/web-apps')
    subprocess.run(["git", "clone", "https://github.com/Ramin-Hashemi/ime-app.git"])

    # Change the owner of ime-app directory to ime-app first user
    subprocess.run(["sudo", "chown", "ime-user-1", "/webapps/ime-app"])


def create_virtual_env():
    
    # Command to switch user, change directory, and activate virtual environment
    command = """
    su - ime-user-1 -c '
    cd /web-apps/ime-app &&
    # Using vnenv
    # python3.11 -m venv .venv &&
    # source .venv/bin/activate &&
    # 
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    pip install -r requirements.txt
    '
    """
    # Execute the command
    subprocess.run(command, shell=True, executable='/bin/bash')


def create_django_project():

    # Command to switch user, change directory, and create an empty Django project
    command = """
    su - ime-user-1 -c '
    cd /web-apps/ime-app &&
    # Using vnenv
    # python3.11 -m venv .venv &&
    # source .venv/bin/activate &&
    # 
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    django-admin.py &&
    startproject &&
    ime-app
    '
    """
    # Execute the command
    subprocess.run(command, shell=True, executable='/bin/bash')


def configure_postgre_sql():

    # Command to switch user, change directory, and;
    # Create a database user and a new database for the ime-app
    command = """
    su - postgres -c '
    # Using vnenv
    # python3.11 -m venv .venv &&
    # source .venv/bin/activate &&
    # 
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    sudo createuser --interactive -P
    sudo createdb --owner ime-app-db-user ime_app_db
    sudo logout
    '
    """
    # Execute the command
    subprocess.run(command, shell=True, executable='/bin/bash')


    # Command to switch user, change directory, and;
    # Install database adapter
    command = """
    su - ime-user-1 -c '
    cd /web-apps/ime-app &&
    # Using vnenv
    # python3.11 -m venv .venv &&
    # source .venv/bin/activate &&
    # 
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    pip install psycopg2
    '
    """
    # Execute the command
    subprocess.run(command, shell=True, executable='/bin/bash')


    # Configure the databases section in your settings.py
    config_content = """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hello',
        'USER': 'ime-ai',
        'PASSWORD': '1Ak5RTQt7mtw0OREsfPhJYzXIak41gnrm5NWYEosCeIduJck10awIzoys1wvbL8',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}
"""
    script_path = "/home/webapps/ime-ai/settings.py"
    
    with open("/tmp/settings.py", "w") as f:
        f.write(config_content)
    subprocess.run(["sudo", "mv", "/tmp/settings.py", script_path])

    
    # Build the initial database for Django
    command = """
    su - ime-user-1 -c '
    cd /web-apps/ime-app &&
    # Using vnenv
    # python3.11 -m venv .venv &&
    # source .venv/bin/activate &&
    # 
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    python &&
    manage.py &&
    migrate
    '
    """
    # Execute the command
    subprocess.run(command, shell=True, executable='/bin/bash')


def configure_gunicorn():
    os.chdir('/webapps/ime-app')

    # Create a file to define the parameters you’ll use when running Gunicorn.
    config_content = """
#!/bin/bash

NAME=ime-app
DJANGODIR=/webapps/ime-app/ime-user-1
SOCKFILE=/webapps/ime-app/run/gunicorn.sock
USER=ime-user-1
GROUP=ime-users
NUM_WORKERS=3
WORKER_CLASS=uvicorn.workers.UvicornWorker
VENV=$DIR/.venv/bin/activate
DJANGO_SETTINGS_MODULE=hello.settings
DJANGO_WSGI_MODULE=hello.wsgi
LOG_LEVEL=error

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source $VENV
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn main:app \
  --name $NAME \
  --user=$USER --group=$GROUP \
  --workers $NUM_WORKERS \
  --worker-class $WORKER_CLASS \
  --bind=unix:$SOCKFILE \
  --log-level=$LOG_LEVEL \
  --log-level=debug \
  --log-file=-
"""

    script_path = "/web-apps/ime-app/gunicorn_start"
    
    with open("/tmp/gunicorn_start", "w") as f:
        f.write(config_content)
    subprocess.run(["sudo", "mv", "/tmp/gunicorn_start", script_path])
    
    # Activate the virtual environment and,
    # Make the gunicorn_start script executable.
    activate_script = os.path.join('.venv', 'bin', 'activate')
    subprocess.run(f"source {activate_script} && sudo chmod u+x /home/webspps/ime-ai/gunicorn_start", shell=True, executable='/bin/bash')

    # Create a run folder in your project directory for the Unix socket file
    subprocess.run(["sudo", "mkdir", "-p", "run"])


def configure_supervisor():
    os.chdir('/home/one-user/web-apps/ime-app')

    # Create logs directory
    subprocess.run(["sudo", "mkdir", "-p", "logs"])
    subprocess.run(["sudo", "touch", "-p", "/logs/gunicorn_supervisor.log"])

    # Create a Supervisor configuration file.
    config_content = """
[program:ime-app]
command=/home/one-user/webapps/ime-app/gunicorn_start
user=one-user
autostart=true
autorestart=true
redirect_stderr=true
stderr_logfile=/home/one-user/webapps/ime-app/logs/gunicorn.error.log
stdout_logfile=/home/one-user/webapps/ime-app/logs/gunicorn.log
environment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
"""

    config_path = "/etc/supervisor/conf.d/ime-app.conf"
    with open("/tmp/ime-app.conf", "w") as f:
        f.write(config_content)
    subprocess.run(["sudo", "mv", "/tmp/ime-app.conf", config_path])

    # Activate the virtual environment and,
    # Reread Supervisor’s configuration file and restart the service.
    activate_script = os.path.join('.venv', 'bin', 'activate')
    subprocess.run(f"source {activate_script} && sudo supervisorctl reread ime-app", shell=True, executable='/bin/bash')
    subprocess.run(f"source {activate_script} && sudo supervisorctl update ime-app", shell=True, executable='/bin/bash')
    subprocess.run(f"source {activate_script} && sudo supervisorctl restart ime-app", shell=True, executable='/bin/bash')


def configure_nginx():
    os.chdir('/home/one-user/webapps/ime-app')

    # Create a new NGINX configuration file
    config_content = """
upstream ime_app_server {
    # fail_timeout=0 means we always retry an upstream even if it failed
    # to return a good HTTP response (in case the Unicorn master nukes a
    # single worker for timing out).

    server unix:/home/webapps/ime-ai/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;

    # add here the ip address of your server
    # or a domain pointing to that ip (like example.com or www.example.com)
    server_name 185.213.165.171;

    keepalive_timeout 5;
    client_max_body_size 4G;

    access_log /home/webapps/ime-app/logs/nginx-access.log;
    error_log /home/webapps/ime-app/logs/nginx-error.log;

    location /static/ {
        alias   /webapps/ime-app/static/;
    }    

    location /media/ {
        alias   /webapps/ime-app/media/;
    }    

    location / {
        # an HTTP header important enough to have its own Wikipedia entry:
        #   http://en.wikipedia.org/wiki/X-Forwarded-For
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # enable this if and only if you use HTTPS, this helps Rack
        # set the proper protocol for doing redirects:
        # proxy_set_header X-Forwarded-Proto https;

        # pass the Host: header from the client right along so redirects
        # can be set properly within the Rack application
        proxy_set_header Host $http_host;

        # we don't want nginx trying to do something clever with
        # redirects, we set the Host: header above already.
        proxy_redirect off;

        # set "proxy_buffering off" *only* for Rainbows! when doing
        # Comet/long-poll stuff.  It's also safe to set if you're
        # using only serving fast clients with Unicorn + nginx.
        # Otherwise you _want_ nginx to buffer responses to slow
        # clients, really.
        # proxy_buffering off;

        # Try to serve static files from nginx, no point in making an
        # *application* server like Unicorn/Rainbows! serve static files.
        if (!-f $request_filename) {
            proxy_pass http://ime_app_server;
            break;
        }
    }

    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /webapps/ime-app/static/;
    }
}
"""
    with open("/etc/nginx/sites-available/ime-app", "w") as config_file:
        config_file.write(config_content)

    # Activate the virtual environment and,
    activate_script = os.path.join('.venv', 'bin', 'activate')

    # Enable the configuration of your site by creating a symbolic link from the file in sites-available into sites-enabled
    subprocess.run("sudo", "ln" "-s" "/etc/nginx/sites-available/ime-app" "/etc/nginx/sites-enabled/ime-app")

    # If you get a permission error telling you that NGINX cannot access the unix socket, you can add the www-data user
    subprocess.run("sudo", "usermod", "-aG", "one-user", "www-data")

    # Restart NGINX
    subprocess.run("sudo", "systemctl", "restart", "nginx")
    subprocess.run("sudo", "service", "restart", "nginx")


def ssl_certificate_certbot():
    os.chdir('/home/one-user/web-apps/ime-app')

    # Install Certbot
    subprocess.run(["sudo", "snap", "install", "--classic", "certbot"])
    subprocess.run(["sudo", "ln", "-s", "/snap/bin/certbot", "/usr/bin/certbot"])

    # Generate a certificate for your domain
    subprocess.run(["sudo", "certbot", "--nginx"])

    # Certbot will automatically handle the renewal of your certificate. To test that it works, run the following:
    subprocess.run(["sudo", "certbot", "renew", "--dry-run"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a function name to run.")
        sys.exit(1)
    
    function_name = sys.argv[1]
    if function_name == "prepare_server":
        prepare_server()
    else:
        print(f"Function {function_name} not found.")