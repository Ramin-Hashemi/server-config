########################
# File serverConfig.py #
########################


import subprocess
import secret
import sys
import os


def ime_app_server_configurations():
    install_packages()
    unattended_upgrades()
    clone_github_repository()
    create_new_users()
    # secure_server()
    # create_virtual_env()
    # create_django_project()
    # configure_gunicorn()
    # configure_supervisor()
    # configure_nginx()
    # ssl_certificate_certbot()


def install_packages():
    command = """
    su - root -c '
    # Update package lists
    sudo apt-get update -y

    # Upgrade all packages
    sudo apt-get upgrade -y

    # Projects required packages
    sudo apt-get install -y unattended-upgrades
    sudo apt-get install -y build-essential
    sudo apt-get install -y checkinstall
    sudo apt-get install -y coreutils
    sudo apt-get install -y libreadline-gplv2-dev
    sudo apt-get install -y libncurses-dev
    sudo apt-get install -y libncursesw5-dev
    sudo apt-get install -y libssl-dev
    sudo apt-get install -y libsqlite3-dev
    sudo apt-get install -y tk-dev
    sudo apt-get install -y libgdbm-dev
    sudo apt-get install -y libc6-dev
    sudo apt-get install -y libbz2-dev
    sudo apt-get install -y zlib1g-dev
    sudo apt-get install -y openssl
    sudo apt-get install -y libffi-dev
    sudo apt-get install -y software-properties-common
    sudo systemctl enable --now snapd.socket
    sudo apt-get install -y uuid-dev
    sudo apt-get install -y lzma-dev
    sudo apt-get install -y wget
    sudo apt-get install -y tree
    sudo apt-get install -y curl
    sudo apt-get install -y vim
    sudo apt-get install -y ca-certificates
    sudo apt-get install -y lsb-release
    sudo apt-get install -y gnupg
    sudo apt-get install -y python3-pip
    sudo pip install --upgrade pip
    sudo apt-get install -y python3-setuptools
    sudo apt-get install -y virtualenv
    sudo apt-get install -y git

    # Add the deadsnakes PPA for newer Python versions
    sudo add-apt-repository ppa:deadsnakes/ppa -y

    # Install Python 3.11 and related packages
    sudo apt-get install -y python3.11
    sudo apt-get install -y python3.11-venv
    sudo apt-get install -y python-virtualenv

    # Building Python modules
    sudo apt-get install -y python3-dev

    # Install PostgreSQL
    sudo apt-get install -y postgresql
    sudo apt-get install -y postgresql-contrib

    # Library for communication with Postgres
    sudo apt-get install -y libpq-dev

    # Dependencies
    sudo pip install pexpect
    sudo pip install python-dotenv
    sudo apt-get install -y snapd
    sudo systemctl enable --now snapd.socket
    sudo snap install core
    sudo snap refresh core
    sudo apt-get install -y policycoreutils-python-utils

    # Install Supervisor and NGINX
    sudo apt-get install -y supervisor
    sudo apt-get install -y nginx
    sudo systemctl enable supervisor
    sudo systemctl start supervisor

    # Install Resetter
    sudo add-apt-repository ppa:resetter/ppa -y
    sudo apt-get install -y resetter

    # Install npm (JavaScript package manager)
    sudo apt-get install -y npm

    # Install Ollama
    npm install ollama

    # Install Docker
    # Add Docker's official GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Set up the stable repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Install Docker Engine
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    # Update package lists
    sudo apt-get update -y

    # Upgrade all packages
    sudo apt-get upgrade -y
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<install_packages> function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e.stderr)


def unattended_upgrades():
    # Configure unattended-upgrades to run automatically
    command = """
    su - root -c '
    echo "APT::Periodic::Update-Package-Lists \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades &&
    echo "APT::Periodic::Unattended-Upgrade \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades &&
    echo "APT::Periodic::AutocleanInterval \\"7\\";" >> /etc/apt/apt.conf.d/20auto-upgrades &&
    sed -i \'s|//Unattended-Upgrade::Automatic-Reboot "false";|Unattended-Upgrade::Automatic-Reboot "true";|\' /etc/apt/apt.conf.d/50unattended-upgrades
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<unattended_upgrades> function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e.stderr)


def clone_github_repository():
    # Command to switch root user
    command = """
    su - root -c '
    sudo mkdir -p /home/web-apps &&                                                 # Create a directory to store web applications on server
    cd /home/web-apps &&                                                            # Change directory to web-apps
    git clone https://github.com/Ramin-Hashemi/ime-app.git                          # Clone iME project from GitHub
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<clone_github_repository> function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e.stderr)


def create_new_users():
    command = """
    su - root -c '
    useradd --system ime-app-server-admin &&                                # Create a new user
    groupadd --system ime-app-group &&                                      # Create a new user group
    gpasswd -a ime-app-server-admin ime-app-group &&                        # Add the new user to the new group
    gpasswd -a ime-app-group sudo &&                                        # Add the new group to the sudo group
    usermod --shell /bin/bash ime-app-server-admin &&                       # Set the shell for the user
    usermod --home /home/web-apps/ime-app ime-app-server-admin &&           # Set the home directory for the user
    chown ime-app-server-admin /home/web-apps/ime-app                       # Change the owner of ime-app directory
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<create_new_users> function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e.stderr)


def secure_server():
    # Set up your server so that you connect to it using an SSH key instead of a password.
    os.chdir('/home/webapps')
    subprocess.run(['sudo', 'mkdir', '-p', '/home/web-apps/.ssh'])
    subprocess.run(['sudo', 'chmod', '700', '/home/web-apps/.ssh'])
    subprocess.run(['sudo', 'chmod', '600', '/home/web-apps/.ssh/authorized_keys'])
    subprocess.run(f'sudo bash -c \'echo "{secret.Public_SSH_key}" >> /home/web-apps/.ssh/authorized_keys\'', shell=True)

    # Disable the root login and password authentication rather than an SSH key for SSH connections.
    subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PubkeyAuthentication .*|PubkeyAuthentication yes|', '/etc/ssh/sshd_config'])
    # subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PermitRootLogin .*|PermitRootLogin no|', '/etc/ssh/sshd_config'])
    # subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PasswordAuthentication .*|PasswordAuthentication no|', '/etc/ssh/sshd_config'])


def create_virtual_env():
    
    # Command to switch user, change directory, and activate virtual environment
    command = """
    su - ime-user-1 -c '
    cd /home/web-apps/ime-app &&
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
    su - ime-user-super-admin -c '
    cd /home/web-apps/ime-app &&
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    django-admin.py &&
    startproject &&
    ime-app-django
    '
    """
    # Execute the command
    subprocess.run(command, shell=True, executable='/bin/bash')


def configure_postgre_sql():

    # Command to switch user, change directory, and;
    # Create a database user and a new database for the ime-app
    command = """
    su - postgres -c '
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    sudo createuser --interactive -P &&
    sudo createdb --owner ime-app-db-user ime_app_db &&
    sudo logout
    '
    """
    # Execute the command
    subprocess.run(command, shell=True, executable='/bin/bash')


    # Command to switch user, change directory, and;
    # Install database adapter
    command = """
    su - ime-user-1 -c '
    cd /home/web-apps/ime-app &&
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
        'NAME': 'ime_app_db',
        'USER': 'ime-app-db-user',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}
"""
    script_path = "/home/web-apps/ime-app/ime-app-settings/settings.py"
    
    with open("/tmp/settings.py", "w") as f:
        f.write(config_content)
    subprocess.run(["sudo", "mv", "/tmp/settings.py", script_path])

    
    # Build the initial database for Django
    command = """
    su - ime-user-1 -c '
    cd /home/web-apps/ime-app &&
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
    os.chdir('/home/web-apps/ime-app')

    # Create a file to define the parameters when running Gunicorn.
    config_content = """
#!/bin/bash

NAME=ime-app-gunicorn                                   # Name of the application
DJANGODIR=/home/we-apps/ime-app-django                  # Django project directory
SOCKFILE=/home/web-apps/ime-app/run/gunicorn.sock       # we will communicte using this unix socket
USER=ime-user-1                                         # the user to run as
GROUP=ime-users                                         # the group to run as
NUM_WORKERS=3                                           # how many worker processes should Gunicorn spawn
WORKER_CLASS=uvicorn.workers.UvicornWorker
VENV=$DIR/bin/activate
DJANGO_SETTINGS_MODULE=ime-app-django.settings          # which settings file should Django use
DJANGO_WSGI_MODULE=ime-app-django.wsgi                  # WSGI module name
LOG_LEVEL=error

echo "Starting $NAME as `iME Agent`"

# Activate the virtual environment
cd $DJANGODIR
source $VENV
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory in the project directory for the Unix socket file if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --user=$USER --group=$GROUP \
  --workers $NUM_WORKERS \
  --worker-class $WORKER_CLASS \
  --bind=unix:$SOCKFILE \
  --log-level=$LOG_LEVEL \
  --log-file=-
"""

    script_path = "/home/web-apps/ime-app/bin/gunicorn_start"
    
    with open("/tmp/gunicorn_start", "w") as f:
        f.write(config_content)
    subprocess.run(["sudo", "mv", "/tmp/gunicorn_start", script_path])
    
    # Activate the virtual environment and,
    # Make the gunicorn_start script executable.
    activate_script = os.path.join('bin', 'activate')
    subprocess.run(f"source {activate_script} && sudo chmod u+x /home/web-apps/ime-app/bin/gunicorn_start", shell=True, executable='/bin/bash')


def configure_supervisor():
    os.chdir('/home/ime-user-1/web-apps/ime-app')

    # Create logs directory
    subprocess.run(["sudo", "mkdir", "-p", "logs"])
    subprocess.run(["sudo", "touch", "-p", "/logs/gunicorn_supervisor.log"])

    # Create a Supervisor configuration file.
    config_content = """
[program:ime-app]
command=/web-apps/ime-app/bin/gunicorn_start
user=ime-app-super-admin
autostart=true
autorestart=true
stdout_logfile=/home/web-apps/ime-app/logs/gunicorn-supervisor.log
redirect_stderr=true
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
    if function_name == "ime_app_server_configurations":
        ime_app_server_configurations()
    else:
        print(f"Function {function_name} not found.")