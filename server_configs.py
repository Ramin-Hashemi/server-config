########################
# File serverConfig.py #
########################


import subprocess
import secret
import sys
import os


def run():
    install_packages()
    clone_github_repository()
    # create_new_users()
    # secure_server()
    # create_virtual_env()
    # create_django_project()
    # create_postgres_database()
    # database_adapter()
    # database_settings()
    # build_django_database()
    # config_gunicorn()
    # config_supervisor()
    # config_nginx()
    # ssl_certificate_certbot()


def install_packages():
    command = """
    su - root -c '
    # Update package lists
    apt-get update -y

    # Upgrade all packages
    sudo apt-get upgrade -y

    # Projects required packages
    # To be reviewed ??????
    apt-get install -y build-essential
    apt-get install -y checkinstall
    apt-get install -y coreutils
    apt-get install -y libreadline-gplv2-dev
    apt-get install -y libncurses-dev
    apt-get install -y libncursesw5-dev
    apt-get install -y libssl-dev
    apt-get install -y libsqlite3-dev
    apt-get install -y tk-dev
    apt-get install -y libgdbm-dev
    apt-get install -y libc6-dev
    apt-get install -y libbz2-dev
    apt-get install -y zlib1g-dev
    apt-get install -y openssl
    apt-get install -y libffi-dev
    apt-get install -y software-properties-common
    apt-get install -y uuid-dev
    apt-get install -y lzma-dev
    apt-get install -y wget
    apt-get install -y tree
    apt-get install -y curl
    apt-get install -y vim
    apt-get install -y ca-certificates
    apt-get install -y lsb-release
    apt-get install -y gnupg
    
    # Install Python 3.13 and related packages
    apt-get install -y python3.13
    apt-get install -y python3-pip
    apt-get install -y python3-setuptools
    apt-get install -y python3.13-venv
    apt-get install -y python-virtualenv
    apt-get install -y policycoreutils-python-utils
    pip install python-dotenv

    # Building Python modules
    apt-get install -y python3-dev

    # Install PostgreSQL
    apt-get install -y postgresql
    apt-get install -y postgresql-contrib

    # Library for communication with Postgres
    apt-get install -y libpq-dev

    # snapd universal package management
    apt-get install -y snapd
    systemctl enable --now snapd.socket
    snap install core
    snap refresh core

    # Add the deadsnakes PPA for newer Python versions
    add-apt-repository ppa:deadsnakes/ppa -y

    # Install Supervisor and NGINX
    apt-get install -y supervisor
    apt-get install -y nginx
    systemctl enable supervisor
    systemctl start supervisor

    # Install Ollama
    npm install ollama

    # Update package lists
    apt-get update -y

    # Upgrade all packages
    apt-get upgrade -y
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<install_packages>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<install_packages>>>>> Error occurred:", e.stderr)


def clone_github_repository():
    command = f"""
    su - root -c '
    mkdir -p /home/web-apps &&
    cd /home/web-apps &&
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL}
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<clone_github_repository>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<clone_github_repository>>>>> Error occurred:", e.stderr)


def create_new_users():
    command = """
    # Variables
    GROUP_NAME="ime-app-group"
    user="ime-app-server-admin"
    USER_HOME="/home/web-apps"
    USER_SHELL="/bin/bash"

    # Check if group exists, if not, create it
    if ! getent group "$GROUP_NAME" > /dev/null 2>&1; then
        groupadd "$GROUP_NAME"
        echo "Group $GROUP_NAME created."
    else
        echo "Group $GROUP_NAME already exists."
    fi

    # Check if user exists, if not, create it
    if ! id -u "$user" > /dev/null 2>&1; then
        useradd --system --gid "$GROUP_NAME" --shell "$USER_SHELL" --home "$USER_HOME" "$user"
        echo "User $user created."
    else
        echo "User $user already exists."
    fi
    """

    try:
        # Execute the command as root
        result = subprocess.run(['su', '-', 'root', '-c', command], check=True, capture_output=True, text=True)
        print("<create_new_users>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_new_users>>>>> Error occurred:", e.stderr)


def secure_server():
    # Set up your server so that you connect to it using an SSH key instead of a password
    command = """
    su - root -c '
    mkdir -p /home/web-apps/.ssh &&
    chmod 700 /home/web-apps/.ssh &&
    chmod 600 /home/web-apps/.ssh/authorized_keys &&
    echo "{secret.Public_SSH_key}" >> /home/web-apps/.ssh/authorized_keys &&
    sed -i s|^#\\?PubkeyAuthentication .*|PubkeyAuthentication yes| /etc/ssh/sshd_config &&
    sed -i s|^#\\?PasswordAuthentication .*|PasswordAuthentication yes| /etc/ssh/sshd_config &&
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<secure_server>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<secure_server>>>>> Error occurred:", e.stderr)


def create_virtual_env():
    # Command to switch user, change directory, and activate virtual environment
    command = """
    su - ime-app-super-admin -c '
    cd /home/web-apps/ime-app &&
    # Using venv
    python3 -m venv venv &&
    source venv/bin/activate &&
    pip install -r requirements.txt
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<create_virtual_env>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_virtual_env>>>>> Error occurred:", e.stderr)


def create_django_project():
    # Command to switch user, change directory, and create an empty Django project
    command = """
    su - ime-app-super-admin -c '
    cd /home/web-apps/ime-app &&
    # Using venv
    python3 -m venv venv &&
    source venv/bin/activate &&
    django-admin.py &&
    startproject &&
    ime-app-django
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<create_django_project>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_django_project>>>>> Error occurred:", e.stderr)


def create_postgres_database():
    # Command to switch user, change directory, and;
    # Create a new database user and a new database for the ime-app
    command = """
    su - postgres -c '
    # Using venv
    python3 -m venv venv &&
    source venv/bin/activate &&
    sudo createuser --interactive -P &&
    sudo createdb --owner ime-app-db-admin ime_app_db &&
    sudo logout
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<create_postgres_database>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_postgres_databasel>>>>> Error occurred:", e.stderr)


def database_adapter():
    # Command to switch user, change directory, and;
    # Install database adapter
    command = """
    su - ime-app-super-admin -c '
    cd /home/web-apps/ime-app &&
    # Using venv
    python3 -m venv venv &&
    source venv/bin/activate &&
    pip install psycopg2
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<database_adapter>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<database_adapter>>>>> Error occurred:", e.stderr)


def database_settings():
    # Configure the databases section in your settings.py
    config_content = """
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ime_app_db',
        'USER': 'ime-app-db-admin',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}
"""
    try:
        # Execute the command
        script_path = "/home/web-apps/ime-app/ime-app-settings/settings.py"
        with open("/tmp/settings.py", "w") as f:
            f.write(config_content)
        result = subprocess.run("sudo", "mv", "/tmp/settings.py", {script_path}, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<database_settings>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<database_settings>>>>> Error occurred:", e.stderr)


def build_django_database():
    # Build the initial database for Django
    command = """
    su - ime-app-super-admin -c '
    cd /home/web-apps/ime-app &&
    # Using venv
    python3 -m venv venv &&
    source venv/bin/activate &&
    python &&
    manage.py &&
    migrate
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<build_django_database>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<build_django_database>>>>> Error occurred:", e.stderr)


def config_gunicorn():
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
    try:
        # Execute the command
        script_path = "/home/web-apps/ime-app/bin/gunicorn_start"
        with open("/tmp/gunicorn_start", "w") as f:
            f.write(config_content)
        result = subprocess.run("sudo", "mv", "/tmp/gunicorn_start", {script_path}, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<config_gunicorn>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<config_gunicorn>>>>> Error occurred:", e.stderr)

    # Activate the virtual environment and,
    # Make the gunicorn_start script executable.
    command = """
    su - ime-app-super-admin -c '
    cd /home/web-apps/ime-app &&
    # Using venv
    python3 -m venv venv &&
    source venv/bin/activate &&
    sudo chmod u+x /home/web-apps/ime-app/bin/gunicorn_start
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<config_gunicorn>>>>> Activated successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<config_gunicorn>>>>> Activation error occurred:", e.stderr)


def config_supervisor():
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


def config_nginx():
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
    if function_name == "run":
        run()
    else:
        print(f"Function {function_name} not found.")