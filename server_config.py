########################
# File serverConfig.py #
########################


import subprocess
import secret
import sys
import os


def make_server_ready():
    # install_packages()
    # unattended_upgrades()
    # create_new_user()
    # secure_server()
    # install_software_tools()
    # clone_repo()
    create_virtual_env()
    configure_gunicorn()
    configure_supervisor()
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
    subprocess.run(["sudo", "apt-get", "install", "-y", "libpq-dev"])
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
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-dev"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-setuptools"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "git"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "postgresql"])

    # Not Included by Default:
    subprocess.run(["sudo", "pip", "install", "pexpect"])
    subprocess.run(["sudo", "pip", "install", "python-dotenv"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "snapd"])
    subprocess.run(["sudo", "systemctl", "enable", "--now", "snapd.socket"])
    subprocess.run(["sudo", "snap", "install", "core"])
    subprocess.run(["sudo", "snap", "refresh", "core"])


def unattended_upgrades():
    # Configure unattended-upgrades so that it runs automatically.
    subprocess.run('sudo bash -c \'echo "APT::Periodic::Update-Package-Lists \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades\'', shell=True)
    subprocess.run('sudo bash -c \'echo "APT::Periodic::Unattended-Upgrade \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades\'', shell=True)
    subprocess.run('sudo bash -c \'echo "APT::Periodic::AutocleanInterval \\"7\\";" >> /etc/apt/apt.conf.d/20auto-upgrades\'', shell=True)
    # System automatically reboots when kernel updates require it
    subprocess.run('sudo sed -i \'s|//Unattended-Upgrade::Automatic-Reboot "false";|Unattended-Upgrade::Automatic-Reboot "true";|\' /etc/apt/apt.conf.d/50unattended-upgrades', shell=True)


def create_new_user():
    subprocess.run(["sudo", "adduser", "one-user"],)
    subprocess.run(["sudo", "gpasswd", "-a", "one-user", "sudo"],)
    # subprocess.run(["sudo", "-i", "-u", "one-user"],) # Log in as one-user
    # subprocess.run(["su", "-", "one-user"],) # Log in as one-user


def secure_server():
    # Set up your server so that you connect to it using an SSH key instead of a password.
    os.chdir('/home/one-user')
    subprocess.run(['sudo', 'mkdir', '-p', '/home/one-user/.ssh'])
    subprocess.run(['sudo', 'chmod', '700', '/home/one-user/.ssh'])
    subprocess.run(['sudo', 'chmod', '600', '/home/one-user/.ssh/authorized_keys'])
    subprocess.run(f'sudo bash -c \'echo "{secret.Public_SSH_key}" >> /home/one-user/.ssh/authorized_keys\'', shell=True)

    # Disable the root login and password authentication rather than an SSH key for SSH connections.
    subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PubkeyAuthentication .*|PubkeyAuthentication yes|', '/etc/ssh/sshd_config'])
    subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PermitRootLogin .*|PermitRootLogin no|', '/etc/ssh/sshd_config'])
    # subprocess.run(['sudo', 'sed', '-i', 's|^#\\?PasswordAuthentication .*|PasswordAuthentication no|', '/etc/ssh/sshd_config'])


def install_software_tools():
    # Install Python
    subprocess.run(["sudo", "add-apt-repository", "ppa:deadsnakes/ppa", "-y"])
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "python3.11", "python3.11-venv", "-y"])

    # Install Resetter
    # subprocess.run(["sudo", "add-apt-repository", "ppa:resetter/ppa", "-y"])
    # subprocess.run(["sudo", "apt-get", "update"])
    # subprocess.run(["sudo", "apt-get", "install", "resetter", "-y"])

    # Install Supervisor and NGINX
    subprocess.run(["sudo", "apt-get", "install", "supervisor", "nginx", "-y"])
    subprocess.run(["sudo", "systemctl", "enable", "supervisor"])
    subprocess.run(["sudo", "systemctl", "start", "supervisor"])

    # Install JS
    subprocess.run(["sudo", "apt-get", "install", "-y", "npm"])
    subprocess.run(["npm", "install", "ollama"])

def install_docker():
    # Add Docker's official GPG key
    subprocess.run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg", shell=True)

    # Set up the stable repository
    subprocess.run('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null', shell=True)

    # Install Docker Engine
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"])


def clone_repo():
    os.chdir('/home/one-user')
    subprocess.run(["git", "clone", "https://github.com/Ramin-Hashemi/ime-ai.git"],)


def create_virtual_env():
    os.chdir('/home/one-user/ime-ai')

    # Create the virtual environment
    subprocess.run(["python3.11", "-m", "venv", ".venv"])

    # Activate the virtual environment and install requirements
    activate_script = os.path.join('.venv', 'bin', 'activate')
    subprocess.run(f"source {activate_script} && pip install -r requirements.txt", shell=True, executable='/bin/bash')

def configure_gunicorn():
    os.chdir('/home/one-user/ime-ai')
    
    # Activate the virtual environment and,
    # Create a file to define the parameters you’ll use when running Gunicorn.
    activate_script = os.path.join('.venv', 'bin', 'activate')

    config_content = """
#!/bin/bash

NAME=fastapi-app
DIR=/home/one-user/ime-ai
USER=one-user
GROUP=one-user
WORKERS=3
WORKER_CLASS=uvicorn.workers.UvicornWorker
VENV=$DIR/.venv/bin/activate
BIND=unix:$DIR/run/gunicorn.sock
LOG_LEVEL=error

cd $DIR
source $VENV

exec gunicorn main:app \
  --name $NAME \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-

"""
    script_path = "/home/one-user/ime-ai/gunicorn_start"
    
    with open("/tmp/gunicorn_start", "w") as f:
        f.write(config_content)
    subprocess.run(["sudo", "mv", "/tmp/gunicorn_start", script_path])
    

    # Make the gunicorn_start script executable
    subprocess.run(f"source {activate_script} && sudo chmod u+x gunicorn_start", shell=True, executable='/bin/bash')

    # Create a run folder in your project directory for the Unix socket file
    subprocess.run(["sudo", "mkdir", "-p", "run"])


def configure_supervisor():
    os.chdir('/home/one-user/ime-ai')

    # Create logs directory
    subprocess.run(["sudo", "mkdir", "-p", "logs"])

    # Activate the virtual environment and,
    # Create a Supervisor configuration file.
    activate_script = os.path.join('.venv', 'bin', 'activate')

    config_content = """
[program:fastapi-app]
command=/home/one-user/ime-ai/gunicorn_start
directory=/home/one-user/ime-ai
user=one-user
autostart=true
autorestart=true
redirect_stderr=true
stderr_logfile=/home/one-user/ime-ai/logs/gunicorn.err.log
stdout_logfile=/home/one-user/ime-ai/logs/gunicorn.log
"""

    config_path = "/etc/supervisor/conf.d/fastapi-app.conf"
    with open("/tmp/fastapi-app.conf", "w") as f:
        f.write(config_content)
    subprocess.run(["sudo", "mv", "/tmp/fastapi-app.conf", config_path])

    # Reread Supervisor’s configuration file and restart the service
    subprocess.run(f"source {activate_script} && sudo supervisorctl reread", shell=True, executable='/bin/bash')
    subprocess.run(f"source {activate_script} && sudo supervisorctl update", shell=True, executable='/bin/bash')
    subprocess.run(f"source {activate_script} && sudo supervisorctl restart fastapi-app", shell=True, executable='/bin/bash')


def configure_nginx():
    os.chdir('/home/one-user/ime-ai')

    # Create a new NGINX configuration file
    config_content = """
upstream app_server {
    server unix:/home/one-user/ime-ai/run/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;

    # add here the ip address of your server
    # or a domain pointing to that ip (like example.com or www.example.com)
    server_name 185.213.165.171;

    keepalive_timeout 5;
    client_max_body_size 4G;

    access_log /home/one-user/ime-ai/logs/nginx-access.log;
    error_log /home/one-user/ime-ai/logs/nginx-error.log;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        if (!-f $request_filename) {
            proxy_pass http://185.213.165.171;
            break;
        }
    }
}
"""
    with open("/etc/nginx/sites-available/fastapi-app", "w") as config_file:
        config_file.write(config_content)

    # Enable the configuration of your site by creating a symbolic link from the file in sites-available into sites-enabled
    subprocess.run(["sudo", "ln", "-s", "/etc/nginx/sites-available/fastapi-app", "/etc/nginx/sites-enabled/"])

    # If you get a permission error telling you that NGINX cannot access the unix socket, you can add the www-data user
    subprocess.run(["sudo", "usermod", "-aG", "one-user", "www-data"])

    # Restart NGINX
    subprocess.run(["sudo", "systemctl", "restart", "nginx"])


def ssl_certificate_certbot():
    os.chdir('/home/one-user/ime-ai')

    # Install Certbot
    subprocess.run(["sudo", "snap", "install", "--classic", "certbot"])
    subprocess.run(["sudo", "ln", "-s", "/snap/bin/certbot", "/usr/bin/certbot"])

    # Generate a certificate for your domain
    subprocess.run(["sudo", "certbot", "--nginx"])

    # Certbot will automatically handle the renewal of your certificate. To test that it works, run the following:
    subprocess.run(["sudo", "certbot", "renew", "--dry-run"])


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func_name = sys.argv[1]
        if func_name == "make_server_ready":
            make_server_ready()
        else:
            print(f"No function named {func_name} found.")
    else:
        print("Please provide a function name to run.")