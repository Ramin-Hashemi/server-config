#!/bin/bash -x

# ────────────────────────
#     ███╗   ███╗ ███████╗
# ██╗ ████╗ ████║ ██╔════╝
#     ██╔████╔██║ █████╗  
# ██║ ██║╚██╔╝██║ ██╔══╝  
# ██║ ██║ ╚═╝ ██║ ███████╗
# ╚═╝ ╚═╝     ╚═╝ ╚══════╝
# ────────────────────────
# ───────────────────────────────────────────────────────────────
# ██████╗  ██████╗   ██████╗       ██╗ ███████╗ ██████╗ ████████╗
# ██╔══██╗ ██╔══██╗ ██╔═══██╗      ██║ ██╔════╝██╔════╝ ╚══██╔══╝
# ██████╔╝ ██████╔╝ ██║   ██║      ██║ █████╗  ██║         ██║   
# ██╔═══╝  ██╔══██╗ ██║   ██║ ██   ██║ ██╔══╝  ██║         ██║   
# ██║      ██║  ██║ ╚██████╔╝ ╚█████╔╝ ███████╗╚██████╗    ██║   
# ╚═╝      ╚═╝  ╚═╝  ╚═════╝   ╚════╝  ╚══════╝ ╚═════╝    ╚═╝   
# ───────────────────────────────────────────────────────────────Thanks to CoPilot




# The trap command allows you to specify actions to be taken \
# when the script receives certain signals, such as SIGINT (Ctrl+C) or SIGTERM (termination signal).
# This can be useful for cleaning up resources or performing graceful shutdowns.
trap 'echo "Script interrupted!"; exit 1' SIGINT SIGTERM

# Load configuration
source /home/server-config/config.sh

# Function to check dependencies
check_dependencies() {
    command -v docker >/dev/null 2>&1 || { echo >&2 "Docker is required but it's not installed. Aborting."; exit 1; }
    # Add more dependency checks as needed
}

# Function to prepare the server
prepare_server() {
    echo "Updating and upgrading the server..."
    sudo apt-get update && sudo apt-get upgrade -y
    # Add more server preparation steps
}

# Function to run containers
run_containers() {
    echo "Starting containers..."
    docker-compose up -d
    # Add more container management steps
}

# Decrypt the secret
USER=$(cat user.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
GROUP_NAME=$(cat group_name.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
SSH_KEY_PATH=$(cat ssh_key_path.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
PUBLIC_SSH_KEY=$(cat public_ssh_key.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
IP_ADDRESS=$(cat ip_address.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)

# GitHub
GITHUB_USERNAME=$(cat github_username.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
GITHUB_PAT=$(cat github_pat.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)

REPO_URL_1=$(cat repo_url_1.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_2=$(cat repo_url_2.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_3=$(cat repo_url_3.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_4=$(cat repo_url_4.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_5=$(cat repo_url_5.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_6=$(cat repo_url_6.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_7=$(cat repo_url_7.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_8=$(cat repo_url_8.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_9=$(cat repo_url_9.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
REPO_URL_10=$(cat repo_url_10.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)

# Docker Hub Credentials
NAME_REAL=$(cat name_real.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
NAME_EMAIL=$(cat name_email.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)

GROUP_NAME_DOCKER=$(cat group_name_docker.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
HOSTNAME=$(cat hostname.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)

####################

# Configure dpkg
if sudo dpkg --configure -a; then
    echo "dpkg configured successfully."
else
    echo "Failed to configure dpkg." >&2
    exit 1
fi

# Install python3-tqdm
if sudo apt-get install -y python3-tqdm; then
    echo "python3-tqdm installed successfully."
else
    echo "Failed to install python3-tqdm." >&2
    exit 1
fi

# KVM virtualization support
if sudo apt-get install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils; then
    sudo modprobe kvm
    sudo modprobe kvm_amd
    sudo usermod -aG kvm {secret.USER}
    echo "KVM virtualization installed successfully."
else
    echo "Failed to install KVM virtualization." >&2
    exit 1
fi

# Install Packages
if sudo apt-get update -y; then
    sudo apt-get upgrade -y
    sudo add-apt-repository universe -y
    sudo apt-get install curl -y
    sudo apt-get install openssl -y
    sudo apt-get install -y python3-venv
    sudo apt-get install -y build-essential
    sudo apt-get install -y ubuntu-gnome-desktop gnome-terminal gnome-browser-connector
    echo "Packages installed successfully."
else
    echo "Failed to install packages." >&2
    exit 1
fi

####################

# SSL Certificate Certbot

# # Check if certbot is installed
# if command -v certbot &> /dev/null
# then
#     echo "Certbot is already installed."
# else
#     echo "Certbot is not installed. Installing Certbot..."
#     sudo snap install --classic certbot
#     sudo ln -s /snap/bin/certbot /usr/bin/certbot
# fi

# # Generate a certificate for your domain
# echo "Generating certificate for your domain..."
# sudo certbot --nginx

# # Check if the certificate generation was successful
# if [ $? -eq 0 ]; then
#     echo "Certificate generated successfully."
# else
#     echo "Failed to generate certificate."
#     exit 1
# fi

# # Test certificate renewal
# echo "Testing certificate renewal..."
# sudo certbot renew --dry-run

# # Check if the renewal test was successful
# if [ $? -eq 0 ]; then
#     echo "Certificate renewal test successful."
# else
#     echo "Certificate renewal test failed."
#     exit 1
# fi

####################

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Install Nginx if not installed
if command_exists nginx; then
    echo "Nginx is already installed."
else
    echo "Nginx is not installed. Installing Nginx..."
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create directories for SSL certificates if they don't exist
if [ ! -d /etc/ssl/private ]; then
    sudo mkdir -p /etc/ssl/private
fi
if [ ! -d /etc/ssl/certs ]; then
    sudo mkdir -p /etc/ssl/certs
fi

# Generate a self-signed SSL certificate if it doesn't exist
if [ ! -f /etc/ssl/private/nginx-selfsigned.key ] || [ ! -f /etc/ssl/certs/nginx-selfsigned.crt ]; then
    echo "Generating a self-signed SSL certificate..."
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/CN=$IP_ADDRESS"
else
    echo "Self-signed SSL certificate already exists."
fi

# Create SSL configuration snippets if they don't exist
if [ ! -f /etc/nginx/snippets/self-signed.conf ]; then
    echo "Creating SSL configuration snippet..."
    sudo bash -c 'cat > /etc/nginx/snippets/self-signed.conf <<EOF
ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
EOF'
fi

if [ ! -f /etc/nginx/snippets/ssl-params.conf ]; then
    echo "Creating SSL parameters configuration snippet..."
    sudo bash -c 'cat > /etc/nginx/snippets/ssl-params.conf <<EOF
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
ssl_ciphers "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384";
ssl_dhparam /etc/nginx/dhparam.pem;
EOF'
fi

# Generate a Diffie-Hellman group if it doesn't exist
if [ ! -f /etc/nginx/dhparam.pem ]; then
    echo "Generating Diffie-Hellman group..."
    sudo openssl dhparam -out /etc/nginx/dhparam.pem 2048
else
    echo "Diffie-Hellman group already exists."
fi

# Configure Nginx to use SSL
echo "Configuring Nginx to use SSL..."
sudo bash -c 'cat > /etc/nginx/sites-available/default <<EOF
server {
    listen 443 ssl;
    server_name 185.213.165.171;

    include snippets/self-signed.conf;
    include snippets/ssl-params.conf;

    location / {
        try_files \$uri \$uri/ =404;
    }
}

server {
    listen 80;
    server_name 185.213.165.171;

    return 301 https://\$server_name\$request_uri;
}
EOF'

# Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Reload Nginx to apply changes
echo "Reloading Nginx..."
sudo systemctl reload nginx

echo "Nginx is now configured with a self-signed SSL certificate."

####################

# Clone GitHub Repository

# Create directories if they do not exist
if [ ! -d "/home/app-source" ]; then
    mkdir -p /home/app-source
fi

if [ ! -d "/home/images" ]; then
    mkdir -p /home/images
fi

# Change to the app-source directory
cd /home/app-source

# Clone repositories
for repo in $REPO_URL_1 \
    $REPO_URL_2 \
    $REPO_URL_3 \
    $REPO_URL_4 \
    $REPO_URL_5 \
    $REPO_URL_6 \
    $REPO_URL_7 \
    $REPO_URL_8 \
    $REPO_URL_9 \
    $REPO_URL_10; do
    if git clone https://$GITHUB_USERNAME:$GITHUB_PAT@$repo; then
        echo "Successfully cloned $repo"
    else
        echo "Failed to clone $repo" >&2
        exit 1
    fi
done

####################

# Create Admin User

# Variables
USER_HOME="/home"
USER_SHELL="/bin/bash"

# Check if group exists, if not, create it
if ! getent group "$GROUP_NAME" > /dev/null 2>&1; then
    if groupadd "$GROUP_NAME"; then
        echo "Group $GROUP_NAME created."
    else
        echo "Failed to create group $GROUP_NAME" >&2
        exit 1
    fi
else
    echo "Group $GROUP_NAME already exists."
fi

# Check if user exists, if not, create it
if ! id -u "$USER" > /dev/null 2>&1; then
    if useradd --system --gid "$GROUP_NAME" --shell "$USER_SHELL" --home "$USER_HOME" "$USER"; then
        echo "User $USER created."
    else
        echo "Failed to create user $USER" >&2
        exit 1
    fi
else
    echo "User $USER already exists."
fi

####################

# Remove Docker

# Remove conflicting Docker packages
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
    if dpkg -l | grep -q $pkg; then
        if apt-get remove -y $pkg; then
            echo "Successfully removed $pkg"
        else
            echo "Failed to remove $pkg" >&2
            exit 1
        fi
    else
        echo "$pkg is not installed"
    fi
done

# Uninstall Docker Engine, CLI, containerd, and Docker Compose packages
for pkg in docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras; do
    if dpkg -l | grep -q $pkg; then
        if apt-get purge -y $pkg; then
            echo "Successfully purged $pkg"
        else
            echo "Failed to purge $pkg" >&2
            exit 1
        fi
    else
        echo "$pkg is not installed"
    fi
done

# Delete all Docker images, containers, and volumes
if [ -d /var/lib/docker ]; then
    echo "Deleting Docker data..."
    rm -rf /var/lib/docker
    echo "Docker data deleted."
else
    echo "Docker directory does not exist."
fi

if [ -d /var/lib/containerd ]; then
    echo "Deleting containerd data..."
    rm -rf /var/lib/containerd
    echo "containerd data deleted."
else
    echo "containerd directory does not exist."
fi

####################

# Set up Docker's apt Repository

if apt-get update && \
   apt-get install -y ca-certificates curl && \
   install -m 0755 -d /etc/apt/keyrings && \
   curl -fsSLv --insecure --tlsv1.3 https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
   chmod a+r /etc/apt/keyrings/docker.asc && \
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
   apt-get update; then
    echo "Docker's apt repository set up successfully."
else
    echo "Failed to set up Docker's apt repository." >&2
    exit 1
fi

####################

# Docker Engine

# Command to install the Docker packages (latest)
if sudo apt-get update && \
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin; then
    echo "Docker packages installed successfully."
else
    echo "Failed to install Docker packages." >&2
    exit 1
fi

####################

# Gnome Extension

# Install necessary dependencies
if sudo apt-get -y install meson && \
   sudo apt-get install -y gnome-shell-extension-appindicator gir1.2-appindicator3-0.1; then
    echo "Dependencies installed successfully."
else
    echo "Failed to install dependencies." >&2
    exit 1
fi

# Clone the extension repository
if git clone https://github.com/ubuntu/gnome-shell-extension-appindicator.git; then
    echo "Repository cloned successfully."
else
    echo "Failed to clone repository." >&2
    exit 1
fi

# Build and install the extension
if meson gnome-shell-extension-appindicator /tmp/g-s-appindicators-build && \
   ninja -C /tmp/g-s-appindicators-build install; then
    echo "Extension built and installed successfully."
else
    echo "Failed to build and install extension." >&2
    exit 1
fi

# Enable the extension
if gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com; then
    echo "Extension enabled successfully."
else
    echo "Failed to enable extension." >&2
    exit 1
fi

# Clean up
if rm -rf /tmp/gnome-shell-extension-appindicator; then
    echo "Clean up completed successfully."
else
    echo "Failed to clean up." >&2
    exit 1
fi

# Restart GNOME Shell (only necessary under X11)
if [ "$XDG_SESSION_TYPE" = "x11" ]; then
    echo "Restarting GNOME Shell..."
    gnome-shell --replace &
fi

####################

# Initialize pass

# Check if gpg is installed, install if not
if ! command -v gpg &> /dev/null; then
    echo "gpg is not installed. Installing gpg..."
    if sudo apt-get install -y gnupg; then
        echo "gpg installed successfully."
    else
        echo "Failed to install gpg." >&2
        exit 1
    fi
else
    echo "gpg is already installed."
fi

# Check if pass is installed, install if not
if ! command -v pass &> /dev/null; then
    echo "pass is not installed. Installing pass..."
    if sudo apt-get install -y pass; then
        echo "pass installed successfully."
    else
        echo "Failed to install pass." >&2
        exit 1
    fi
else
    echo "pass is already installed."
fi

echo "gpg and pass are installed."

# Generate a new GPG key
echo "Generating a new GPG key..."
gpg --batch --gen-key <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Name-Real: $NAME_REAL
Name-Email: $NAME_EMAIL
Expire-Date: 0
EOF

# Check if GPG key generation was successful
if [ $? -eq 0 ]; then
    echo "GPG key generated successfully."
else
    echo "Failed to generate GPG key." >&2
    exit 1
fi

# Get the GPG key ID
GPG_KEY_ID=$(gpg --list-keys --with-colons | grep '^pub' | cut -d':' -f5 | tail -n1)

# Initialize pass with the GPG key
echo "Initializing pass with GPG key ID: $GPG_KEY_ID"
if pass init "$GPG_KEY_ID"; then
    echo "pass initialized successfully."
else
    echo "Failed to initialize pass." >&2
    exit 1
fi

# Configure Docker to use pass for credential storage
DOCKER_CONFIG_FILE="$HOME/.docker/config.json"
mkdir -p "$(dirname "$DOCKER_CONFIG_FILE")"
if [ -f "$DOCKER_CONFIG_FILE" ]; then
    if jq '.credsStore = "pass"' "$DOCKER_CONFIG_FILE" > "$DOCKER_CONFIG_FILE.tmp" && mv "$DOCKER_CONFIG_FILE.tmp" "$DOCKER_CONFIG_FILE"; then
        echo "Docker configured to use pass for credential storage."
    else
        echo "Failed to configure Docker." >&2
        exit 1
    fi
else
    if echo '{"credsStore": "pass"}' > "$DOCKER_CONFIG_FILE"; then
        echo "Docker configured to use pass for credential storage."
    else
        echo "Failed to configure Docker." >&2
        exit 1
    fi
fi

####################

# Docker Desktop

# Update package list and install docker prerequisites
if sudo apt-get update -y && \
   sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release gnome-terminal; then
    echo "Docker prerequisites installed successfully."
else
    echo "Failed to install Docker prerequisites." >&2
    exit 1
fi

# Add your user to the kvm group in order to access the kvm device
if sudo usermod -aG kvm $USER; then
    echo "User added to kvm group successfully."
else
    echo "Failed to add user to kvm group." >&2
    exit 1
fi

# Update package list again
if sudo apt-get update -y; then
    echo "Package list updated successfully."
else
    echo "Failed to update package list." >&2
    exit 1
fi

# Install Docker Desktop dependencies
if sudo apt-get install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager libsubid4 uidmap; then
    echo "Docker Desktop dependencies installed successfully."
else
    echo "Failed to install Docker Desktop dependencies." >&2
    exit 1
fi

# Download and Install the latest Docker Desktop DEB package
if wget -O latest-package.deb https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb && \
   sudo dpkg -i latest-package.deb && \
   sudo apt-get install -f; then
    echo "Docker Desktop DEB package installed successfully."
else
    echo "Failed to install Docker Desktop DEB package." >&2
    exit 1
fi

# Enable and start Docker Desktop service
if systemctl --user enable docker-desktop && \
   systemctl --user start docker-desktop; then
    echo "Docker Desktop service enabled and started successfully."
else
    echo "Failed to enable and start Docker Desktop service." >&2
    exit 1
fi

####################

# Docker Post Install

# Check if group exists, if not, create it
if ! getent group "$GROUP_NAME_DOCKER" > /dev/null 2>&1; then
    if groupadd "$GROUP_NAME_DOCKER"; then
        echo "Group $GROUP_NAME_DOCKER created."
    else
        echo "Failed to create group $GROUP_NAME_DOCKER."
        exit 1
    fi
else
    echo "Group $GROUP_NAME_DOCKER already exists."
fi

# Add user to the docker group
if usermod -aG "$GROUP_NAME_DOCKER" "$USER"; then
    echo "User $USER added to group $GROUP_NAME_DOCKER."
else
    echo "Failed to add user $USER to group $GROUP_NAME_DOCKER."
    exit 1
fi

# Activate the changes to groups
if newgrp "$GROUP_NAME_DOCKER"; then
    echo "Group changes activated."
else
    echo "Failed to activate group changes."
    exit 1
fi

# Change ~/.docker/ directory ownership and permissions
if chown "$USER":"$GROUP_NAME_DOCKER" /root/.docker -R && chmod g+rwx "/root/.docker" -R; then
    echo "Ownership and permissions for ~/.docker/ changed."
else
    echo "Failed to change ownership and permissions for ~/.docker/."
    exit 1
fi

# To automatically start Docker and containerd on boot
if systemctl enable docker.service && systemctl enable containerd.service; then
    echo "Docker and containerd services enabled to start on boot."
else
    echo "Failed to enable Docker and containerd services."
    exit 1
fi

# Remove existing symlink if it exists
if [ -L /usr/bin/docker ]; then
    sudo rm /usr/bin/docker
fi

# Create the symbolic link
if ln -s /usr/local/bin/com.docker.cli /usr/bin/docker; then
    echo "Symlink created: /usr/bin/docker -> /usr/local/bin/com.docker.cli"
else
    echo "Failed to create symlink."
    exit 1
fi

# Verify the symlink creation
if [ -L /usr/bin/docker ]; then
    echo "Symlink verified: /usr/bin/docker -> /usr/local/bin/com.docker.cli"
else
    echo "Symlink verification failed."
    exit 1
fi

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

# Backup the current /etc/hosts file
if cp /etc/hosts /etc/hosts.bak; then
    echo "Backup of /etc/hosts created."
else
    echo "Failed to create backup of /etc/hosts."
    exit 1
fi

# Add the DNS entry to /etc/hosts
if echo "$IP_ADDRESS $HOSTNAME" >> /etc/hosts; then
    echo "DNS entry added: $IP_ADDRESS $HOSTNAME"
else
    echo "Failed to add DNS entry."
    exit 1
fi

# Verify the entry
if grep -q "$HOSTNAME" /etc/hosts; then
    echo "DNS entry verified: $IP_ADDRESS $HOSTNAME"
else
    echo "DNS entry verification failed."
    exit 1
fi

####################

# Secure Server

# Set up your server so that you connect to it using an SSH key instead of a password

# Check if the .ssh directory exists, if not, create it
if [ ! -d "/home/.ssh" ]; then
    if mkdir -p /home/.ssh; then
        echo ".ssh directory created."
    else
        echo "Failed to create .ssh directory."
        exit 1
    fi
else
    echo ".ssh directory already exists."
fi

# Set permissions for the .ssh directory
if chmod 700 /home/.ssh; then
    echo "Permissions set for .ssh directory."
else
    echo "Failed to set permissions for .ssh directory."
    exit 1
fi

# Check if the authorized_keys file, if not, create it
if [ ! -f "/home/.ssh/authorized_keys" ]; then
    if touch /home/.ssh/authorized_keys; then
        echo "authorized_keys file created."
    else
        echo "Failed to create authorized_keys file."
        exit 1
    fi
else
    echo "authorized_keys file already exists."
fi

# Set permissions for the authorized_keys file
if chmod 600 /home/.ssh/authorized_keys; then
    echo "Permissions set for authorized_keys file."
else
    echo "Failed to set permissions for authorized_keys file."
    exit 1
fi

# Add the public SSH key to the authorized_keys file
if echo "$PUBLIC_SSH_KEY" >> /home/.ssh/authorized_keys; then
    echo "Public SSH key added to authorized_keys."
else
    echo "Failed to add public SSH key to authorized_keys."
    exit 1
fi

# Enable PubkeyAuthentication in sshd_config
if sudo sed -i 's|^#\?PubkeyAuthentication .*|PubkeyAuthentication yes|' /etc/ssh/sshd_config; then
    echo "PubkeyAuthentication enabled."
else
    echo "Failed to enable PubkeyAuthentication."
    exit 1
fi

# Enable PasswordAuthentication in sshd_config
if sudo sed -i 's|^#\?PasswordAuthentication .*|PasswordAuthentication yes|' /etc/ssh/sshd_config; then
    echo "PasswordAuthentication enabled."
else
    echo "Failed to enable PasswordAuthentication."
    exit 1
fi

\\ *************************************************************************************************** #

# Main script execution
main() {
    check_dependencies
    prepare_server
    run_containers
}

# Keep the shell open
exec "$SHELL"