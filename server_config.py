#########################
# File server_config.py #
#########################


import subprocess
import secret
import sys
import os
from tqdm import tqdm
import time


def run():
    # install_packages()
    # clone_github_repository()
    # create_admin_user()
    # docker_repository()
    docker_engine()
    # gnome_extension()
    # initialize_pass()
    # docker_desktop()
    # docker_post_install()
    # secure_server()


def install_packages():
    command = """
    su - root -c '
    # Update package lists
    apt-get update -y

    # Upgrade all packages
    apt-get upgrade -y

    # Projects required packages
    apt-get install -y python3-venv
    apt-get install -y python3-tqdm

    # Run the following command to uninstall all conflicting packages
    for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
    
    # Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages
    apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
    
    # To delete all images, containers, and volumes
    rm -rf /var/lib/docker
    rm -rf /var/lib/containerd

    # chrome-gnome-shell and gnome-browser-connector
    apt-get install -y gnome-browser-connector
    '
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="install_packages", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<install_packages>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<install_packages>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<install_packages>>>>> Unexpected error occurred:", str(e))


def clone_github_repository():
    command = f"""
    su - root -c '
    if [ ! -d "/home/app-source" ]; then
      mkdir -p /home/app-source
    fi

    if [ ! -d "/home/images" ]; then
      mkdir -p /home/images
    fi

    cd /home/app-source &&
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_1}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_2}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_3}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_4}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_5}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_6}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_7}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_8}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_9}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_10}
    '
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="clone_github_repository", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<clone_github_repository>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<clone_github_repository>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<create_admin_user>>>>> Unexpected error occurred:", str(e))


def create_admin_user():
    command = """
    su - root -c '
    # Variables
    GROUP_NAME="ime-app-group"
    USER="ime-server-admin"
    USER_HOME="/home"
    USER_SHELL="/bin/bash"

    # Check if group exists, if not, create it
    if ! getent group "$GROUP_NAME" > /dev/null 2>&1; then
        groupadd "$GROUP_NAME"
        echo "Group $GROUP_NAME created."
    else
        echo "Group $GROUP_NAME already exists."
    fi

    # Check if user exists, if not, create it
    if ! id -u "$USER" > /dev/null 2>&1; then
        useradd --system --gid "$GROUP_NAME" --shell "$USER_SHELL" --home "$USER_HOME" "$USER"
        echo "User $USER created."
    else
        echo "User $USER already exists."
    fi
    '
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="create_admin_user", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<create_admin_user>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_admin_user>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<create_admin_user>>>>> Unexpected error occurred:", str(e))


def docker_repository():
    # Set up Docker's apt repository
    command = [
        "sudo", "bash", "-c", """
        # Add Docker's official GPG key:
        apt-get update &&
        apt-get install -y ca-certificates curl &&
        install -m 0755 -d /etc/apt/keyrings &&
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc &&
        chmod a+r /etc/apt/keyrings/docker.asc &&

        # Add the repository to Apt sources:
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null &&
        apt-get update
        """
    ]
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="docker_repository", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<docker_repository>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<docker_repository>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<docker_repository>>>>> Unexpected error occurred:", str(e))


def docker_engine():
    # Command to install the Docker packages (latest)
    command = [
        "sudo", "bash", "-c", """
        apt-get update &&
        apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        """
    ]
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="docker_engine", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<docker_engine>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<docker_engine>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<docker_engine>>>>> Unexpected error occurred:", str(e))


def gnome_extension():
    command = """
    su - root -c '
    # Update package lists
    apt-get update -y

    # Install necessary dependencies
    apt-get install -y gnome-shell-extension-appindicator gir1.2-appindicator3-0.1

    # Clone the extension repository
    git clone https://github.com/ubuntu/gnome-shell-extension-appindicator.git /tmp/gnome-shell-extension-appindicator

    # Checkout the latest version (v59)
    cd /tmp/gnome-shell-extension-appindicator
    git checkout v59

    # Build and install the extension
    meson build
    ninja -C build install

    # Enable the extension
    gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com

    # Clean up
    rm -rf /tmp/gnome-shell-extension-appindicator

    # Restart GNOME Shell (only necessary under X11)
    if [ "$XDG_SESSION_TYPE" = "x11" ]; then
      echo "Restarting GNOME Shell..."
      gnome-shell --replace &
    fi
    '
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="gnome_extension", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<gnome_extension>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<gnome_extension>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<gnome_extension>>>>> Unexpected error occurred:", str(e))


def initialize_pass():
    command = """
    su - root -c '
    # Variables
    NAME_REAL="Ramin-Hashemi"
    NAME_EMAIL="ramin.hashemi.myself@gmail.com"

    # Check if gpg and pass are installed
    if ! command -v gpg &> /dev/null || ! command -v pass &> /dev/null; then
        echo "gpg and pass are required but not installed. Please install them first."
        exit 1
    fi

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

    # Get the GPG key ID
    GPG_KEY_ID=$(gpg --list-keys --with-colons | grep '^pub' | cut -d':' -f5 | tail -n1)

    # Initialize pass with the GPG key
    echo "Initializing pass with GPG key ID: $GPG_KEY_ID"
    pass init "$GPG_KEY_ID"

    # Configure Docker to use pass for credential storage
    DOCKER_CONFIG_FILE="$HOME/.docker/config.json"
    mkdir -p "$(dirname "$DOCKER_CONFIG_FILE")"
    if [ -f "$DOCKER_CONFIG_FILE" ]; then
        jq '.credsStore = "pass"' "$DOCKER_CONFIG_FILE" > "$DOCKER_CONFIG_FILE.tmp" && mv "$DOCKER_CONFIG_FILE.tmp" "$DOCKER_CONFIG_FILE"
    else
        echo '{"credsStore": "pass"}' > "$DOCKER_CONFIG_FILE"
    fi
    '
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="initialize_pass", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<initialize_pass>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<initialize_pass>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<initialize_pass>>>>> Unexpected error occurred:", str(e))


def docker_desktop():
    # Install the Docker packages (latest)
    command = """
    su - root -c '
    # Variables
    USER="ime-server-admin"

    # Update package list and install docker prerequisites
    apt-get update -y
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        gnome-terminal

    # Add your user to the kvm group in order to access the kvm device:
    sudo usermod -aG kvm $USER

    # Add Docker's official GPG key
    install -m 0755 -d /etc/apt/keyrings &&
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc &&
    chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Update package list again
    apt-get update

    # Install Docker Desktop dependencies
    apt-get install -y \
        qemu-kvm \
        libvirt-daemon-system \
        libvirt-clients \
        bridge-utils \
        virt-manager

    # Download and Install the latest Docker Desktop DEB package
    wget -O latest-package.deb https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb &&
    dpkg -i latest-package.deb &&
    apt-get install -f &&

    # Install Docker Desktop
    apt-get update &&
    apt-get install -y ./docker-desktop-amd64.deb &&

    # Enable and start Docker Desktop service
    systemctl --user enable docker-desktop &&
    systemctl --user start docker-desktop &&
    '
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="docker_desktop", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<docker_desktop>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<docker_desktop>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<docker_desktop>>>>> Unexpected error occurred:", str(e))


def docker_post_install():
    command = """
    # Variables
    GROUP_NAME_DOCKER="docker"
    USER="ime-server-admin"

    # Check if group exists, if not, create it
    if ! getent group "$GROUP_NAME_DOCKER" > /dev/null 2>&1; then
        groupadd "$GROUP_NAME_DOCKER"
        echo "Group $GROUP_NAME_DOCKER created."
    else
        echo "Group $GROUP_NAME_DOCKER already exists."
    fi

    usermod -aG $GROUP_NAME_DOCKER $USER

    # Activate the changes to groups
    newgrp $GROUP_NAME_DOCKER

    # Change ~/.docker/ directory ownership and permissions
    chown "$USER":"$USER" /home/"$USER"/.docker -R &&
    chmod g+rwx "$HOME/.docker" -R

    # To automatically start Docker and containerd on boot
    systemctl enable docker.service &&
    systemctl enable containerd.service

    # Check if the source file exists
    if [ ! -f /usr/local/bin/com.docker.cli ]; then
        echo "Source file /usr/local/bin/com.docker.cli does not exist."
        exit 1
    fi

    # Creates a symlink from /usr/local/bin/com.docker.cli to /usr/bin/docker
    # Create the symbolic link
    ln -s /usr/local/bin/com.docker.cli /usr/bin/docker

    # Verify the symlink creation
    if [ -L /usr/bin/docker ]; then
        echo "Symlink created successfully: /usr/bin/docker -> /usr/local/bin/com.docker.cli"
    else
        echo "Failed to create symlink."
        exit 1
    fi

    # Adds a DNS name for Kubernetes to /etc/hosts
    # Check if the script is run as root
    if [ "$EUID" -ne 0 ]; then
        echo "Please run as root"
        exit 1
    fi

    # Variables
    HOSTNAME="kubernetes.local"
    IP_ADDRESS="192.168.1.100"  # Replace with your Kubernetes cluster IP

    # Backup the current /etc/hosts file
    cp /etc/hosts /etc/hosts.bak

    # Add the DNS entry to /etc/hosts
    echo "$IP_ADDRESS $HOSTNAME" >> /etc/hosts

    # Verify the entry
    if grep -q "$HOSTNAME" /etc/hosts; then
        echo "DNS entry added successfully: $IP_ADDRESS $HOSTNAME"
    else
        echo "Failed to add DNS entry."
        exit 1
    fi
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="docker_post_install", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<docker_post_install>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<docker_post_install>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<docker_post_install>>>>> Unexpected error occurred:", str(e))


def secure_server():
    # Set up your server so that you connect to it using an SSH key instead of a password
    command = """
    su - root -c '
    if [ ! -d "/home/.ssh" ]; then
      mkdir -p /home/.ssh
    fi &&
    chmod 700 /home/.ssh &&
    chmod 600 /home/.ssh/authorized_keys &&
    echo "{secret.PUBLIC_SSH_KEY}" >> /home/.ssh/authorized_keys &&
    sed -i s|^#\\?PubkeyAuthentication .*|PubkeyAuthentication yes| /etc/ssh/sshd_config &&
    sed -i s|^#\\?PasswordAuthentication .*|PasswordAuthentication yes| /etc/ssh/sshd_config
    '
    """
    try:
        # Execute the command and show progress
        with tqdm(total=100, desc="secure_server", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
            result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
            for _ in range(10):
                time.sleep(0.1)  # Simulate progress
                pbar.update(10)
        print("<secure_server>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<secure_server>>>>> Error occurred:", e.stderr)
    except Exception as e:
        print("<secure_server>>>>> Unexpected error occurred:", str(e))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a function name to run.")
        sys.exit(1)
    
    function_name = sys.argv[1]
    if function_name == "run":
        run()
    else:
        print(f"Function {function_name} not found.")