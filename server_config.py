########################
# File serverConfig.py #
########################


import subprocess
import secret
import sys
import os


def make_server_ready():
    install_packages()
    unattended_upgrades()
    # create_new_user()
    secure_server()
    install_software_tools()
    clone_repo()
    create_virtual_env()
    configure_gunicorn()
    configure_supervisor()
    configure_nginx()
    # ssl_certificate_certbot()


def install_packages():
    subprocess.run(["sudo", "apt-get", "update", "-y"], check=True)
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "unattended-upgrades"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "build-essential"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "checkinstall"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "coreutils"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libreadline-gplv2-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libncurses-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libncursesw5-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libssl-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libsqlite3-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "tk-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libgdbm-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libpq-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libc6-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libbz2-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "zlib1g-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "openssl"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "libffi-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "snapd"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "software-properties-common"], check=True)
    subprocess.run(["sudo", "snap", "install", "core"], check=True)
    subprocess.run(["sudo", "snap", "refresh", "core"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "--now", "snapd.socket"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "uuid-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "lzma-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "wget"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "tree"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "curl"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "vim"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "ca-certificates"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "lsb-release"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "gnupg"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-pip"], check=True)
    subprocess.run(["sudo", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-dev"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "python3-setuptools"], check=True)
    subprocess.run(["sudo", "pip", "install", "python-dotenv"], check=True)
    subprocess.run(["sudo", "pip", "install", "pexpect"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "git"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "postgresql"], check=True)
    

def unattended_upgrades():
    # Configure unattended-upgrades so that it runs automatically.
    subprocess.run('echo \'APT::Periodic::Update-Package-Lists "1";\' >> /etc/apt/apt.conf.d/20auto-upgrades', shell=True, check=True)
    subprocess.run('echo \'APT::Periodic::Unattended-Upgrade "1";\' >> /etc/apt/apt.conf.d/20auto-upgrades', shell=True, check=True)
    subprocess.run('echo \'APT::Periodic::AutocleanInterval "7";\' >> /etc/apt/apt.conf.d/20auto-upgrades', shell=True, check=True)
    # System automatically reboots when kernel updates require it
    subprocess.run('sudo sed -i \'s|//Unattended-Upgrade::Automatic-Reboot "false";|Unattended-Upgrade::Automatic-Reboot "true";|\' /etc/apt/apt.conf.d/50unattended-upgrades', shell=True, check=True)


def create_new_user():
    subprocess.run(["sudo", "adduser", "one-user"], check=True)
    subprocess.run(["sudo", "gpasswd", "-a", "one-user", "sudo"], check=True)
    # subprocess.run(["sudo", "-i", "-u", "one-user"], check=True) # Log in as one-user


def secure_server():
    # Set up your server so that you connect to it using an SSH key instead of a password.
    os.chdir('/home/one-user')
    subprocess.run(['mkdir', '-p', '/home/one-user/.ssh/'], check=True)
    subprocess.run(['chmod', '700', '/home/one-user/.ssh/'], check=True)
    subprocess.run(f'echo \'{secret.Public_SSH_key}\' >> /home/one-user/.ssh/authorized_keys', shell=True, check=True)

    # Disable the root login and password authentication rather than an SSH key for SSH connections.
    subprocess.run(['sed', '-i', 's|#PermitRootLogin yes|PermitRootLogin no|', '/etc/ssh/sshd_config'], check=True)
    subprocess.run(['sed', '-i', 's|#PasswordAuthentication yes|PasswordAuthentication no|', '/etc/ssh/sshd_config'], check=True)


def install_software_tools():
    # Install Python
    subprocess.run(["sudo", "add-apt-repository", "ppa:deadsnakes/ppa", "-y"], check=True)
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "python3.12", "python3.12-venv", "-y"], check=True)
        
    # Install Resetter
    # subprocess.run(["sudo", "add-apt-repository", "ppa:resetter/ppa", "-y"], check=True)
    # subprocess.run(["sudo", "apt", "update"], check=True)
    # subprocess.run(["sudo", "apt", "install", "resetter", "-y"], check=True)

    # Install Supervisor and NGINX
    subprocess.run(["sudo", "apt-get", "install", "supervisor", "nginx", "-y"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "supervisor"], check=True)
    subprocess.run(["sudo", "systemctl", "start", "supervisor"], check=True)
        
    # Install JS
    subprocess.run(["sudo", "apt-get", "install", "-y", "npm"], check=True)
    subprocess.run(["npm", "i", "ollama"], check=True)
    
def install_docker():
    # Add Docker's official GPG key
    subprocess.run("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg", shell=True, check=True)
    
    # Set up the stable repository
    subprocess.run('echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null', shell=True, check=True)
    
    # Install Docker Engine
    subprocess.run(["sudo", "apt-get", "update"], check=True)
    subprocess.run(["sudo", "apt-get", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"], check=True)


def clone_repo():
    os.chdir('/home/one-user')
    subprocess.run(["git", "clone", "https://github.com/Ramin-Hashemi/ime-ai.git"], check=True)


def create_virtual_env():
    os.chdir('/home/one-user/ime-ai')
    
    # Create the virtual environment
    subprocess.run(["python3.12", "-m", "venv", ".venv"], check=True)
    
    # Activate the virtual environment
    subprocess.run(["/bin/bash", "-c", "source .venv/bin/activate && pip install -r requirements.txt"], check=True)


def configure_gunicorn():
    os.chdir('/home/one-user/ime-ai')
    # Create a file to define the parameters you’ll use when running Gunicorn.
    config_content = """
#!/bin/bash

NAME=fastapi-app
DIR=/home/fastapi-user/fastapi-nginx-gunicorn
USER=fastapi-user
GROUP=fastapi-user
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
    with open("/home/one-user/ime-ai/gunicorn_start", "w") as config_file:
        config_file.write(config_content)
    
    # Make the gunicorn_start script executable
    subprocess.run(["chmod", "u+x", "gunicorn_start"], check=True)
    
    # Create a run folder in your project directory for the Unix socket file
    subprocess.run(["mkdir", "-p", "run"], check=True)


def configure_supervisor():
    os.chdir('/home/one-user/ime-ai')
    
    # Create logs directory
    subprocess.run(["mkdir", "-p", "logs"], check=True)
    
    # Create a Supervisor configuration file
    config_content = """
[program:fastapi-app]
command=/home/one-user/ime-ai/gunicorn_start
user=one-user
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/one-user/ime-ai/logs/gunicorn-error.log
"""
    with open("/etc/supervisor/conf.d/fastapi-app.conf", "w") as config_file:
        config_file.write(config_content)
    
    # Reread Supervisor’s configuration file and restart the service
    subprocess.run(["sudo", "supervisorctl", "reread"], check=True)
    subprocess.run(["sudo", "supervisorctl", "update"], check=True)
    subprocess.run(["sudo", "supervisorctl", "restart", "fastapi-app"])


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
    server_name XXXX;

    keepalive_timeout 5;
    client_max_body_size 4G;

    access_log /home/one-user/ime-ai/logs/nginx-access.log;
    error_log /home/one-user/ime-ai/logs/nginx-error.log;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;

        if (!-f $request_filename) {
            proxy_pass http://app_server;
            break;
        }
    }
}
"""
    with open("/etc/nginx/sites-available/fastapi-app", "w") as config_file:
        config_file.write(config_content)
    
    # Enable the configuration of your site by creating a symbolic link from the file in sites-available into sites-enabled
    subprocess.run(["sudo", "ln", "-s", "/etc/nginx/sites-available/fastapi-app", "/etc/nginx/sites-enabled/"], check=True)
    
    # If you get a permission error telling you that NGINX cannot access the unix socket, you can add the www-data user
    # subprocess.run(["sudo", "usermod", "-aG", "main-user", "www-data"], check=True)
    
    # Restart NGINX
    subprocess.run(["sudo", "systemctl", "restart", "nginx"])


def ssl_certificate_certbot():
    os.chdir('/home/one-user/ime-ai')
    
    # Install Certbot
    subprocess.run(["sudo", "snap", "install", "--classic", "certbot"], check=True)
    subprocess.run(["sudo", "ln", "-s", "/snap/bin/certbot", "/usr/bin/certbot"], check=True)
    
    # Generate a certificate for your domain
    subprocess.run(["sudo", "certbot", "--nginx"], check=True)
    
    # Certbot will automatically handle the renewal of your certificate. To test that it works, run the following:
    subprocess.run(["sudo", "certbot", "renew", "--dry-run"], check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func_name = sys.argv[1]
        if func_name == "make_server_ready":
            make_server_ready()
        else:
            print(f"No function named {func_name} found.")
    else:
        print("Please provide a function name to run.")