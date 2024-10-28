#########################
# File server_config.py #
#########################


import subprocess
import secret
import sys
import os


def run():
    install_packages()
    clone_github_repository()
    create_admin_user()
    docker_repository()
    docker_engine()
    # docker_desktop()
    docker_post_install()


def install_packages():
    command = """
    su - root -c '
    # Update package lists
    apt-get update -y

    # Upgrade all packages
    apt-get upgrade -y

    # Projects required packages
    apt-get install -y python3-venv

    # Run the following command to uninstall all conflicting packages
    for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
    
    # Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages
    apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
    
    # To delete all images, containers, and volumes
    rm -rf /var/lib/docker
    rm -rf /var/lib/containerd
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
    mkdir -p /home/apps-source &&
    mkdir -p /home/images &&
    cd /home/apps-source &&
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_1}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_2}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_3}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_4}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_5}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_6}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_7}
    git clone https://{secret.GITHUB_USERNAME}:{secret.GITHUB_PAT}@{secret.REPO_URL_8}
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<clone_github_repository>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<clone_github_repository>>>>> Error occurred:", e.stderr)


def create_admin_user():
    command = """
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

    # Activate the changes to groups
    newgrp $GROUP_NAME
    """

    try:
        # Execute the command as root
        result = subprocess.run(['su', '-', 'root', '-c', command], check=True, capture_output=True, text=True)
        print("<create_admin_user>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_admin_user>>>>> Error occurred:", e.stderr)


def docker_repository():
    # Set up Docker's apt repository
    command = """
    su - root -c '
    # Add Docker's official GPG key:
    apt-get update
    apt-get install ca-certificates curl
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    # If you use an Ubuntu derivative distro, such as Linux Mint, you may need to use UBUNTU_CODENAME instead of VERSION_CODENAME
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<docker_repository>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<docker_repository>>>>> Error occurred:", e.stderr)


def docker_engine():
    # Install the Docker packages (latest)
    command = """
    su - root -c '
    apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<docker_engine>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<docker_engine>>>>> Error occurred:", e.stderr)


def docker_desktop():
    # Install the Docker packages (latest)
    command = """
    su - root -c '
    modprobe kvm &&
    modprobe kvm_intel &&  # Intel processors
    modprobe kvm_amd &&    # AMD processors

    # If the above commands fail, you can view the diagnostics by running:
    kvm-ok

    # To check if the KVM modules are enabled, run:
    lsmod | grep kvm

    # To check ownership of /dev/kvm, run:
    ls -al /dev/kvm

    # Add your user to the kvm group in order to access the kvm device:
    sudo usermod -aG kvm $user

    apt install gnome-terminal

    # Add Docker's official GPG key:
    apt-get update &&
    apt-get install ca-certificates curl &&
    install -m 0755 -d /etc/apt/keyrings &&
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc &&
    chmod a+r /etc/apt/keyrings/docker.asc &&

    # Add the repository to Apt sources:
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null &&
    apt-get update &&

    # Download and Install the latest DEB package
    wget -O latest-package.deb https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb &&
    dpkg -i latest-package.deb &&
    apt-get install -f &&

    apt-get update &&
    apt-get install -y ./docker-desktop-amd64.deb &&

    systemctl --user start docker-desktop &&
    systemctl --user enable docker-desktop &&
    docker compose version &&
    docker --version &&
    docker version
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<docker_desktop>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<docker_desktop>>>>> Error occurred:", e.stderr)


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
    """

    try:
        # Execute the command as root
        result = subprocess.run(['su', '-', 'root', '-c', command], check=True, capture_output=True, text=True)
        print("<create_admin_user>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_admin_user>>>>> Error occurred:", e.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a function name to run.")
        sys.exit(1)
    
    function_name = sys.argv[1]
    if function_name == "run":
        run()
    else:
        print(f"Function {function_name} not found.")