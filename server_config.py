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
    install_docker()
    install_dependencies()
    create_database()
    start_app()


def install_packages():
    command = """
    su - root -c '
    # Update package lists
    apt-get update -y

    # Upgrade all packages
    sudo apt-get upgrade -y

    # Projects required packages
    apt-get install -y python3-venv
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
    user="ime-server-admin"
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


def install_docker():
    # Install and build the required application dependencies
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
        print("<install_dependencies>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<install_dependencies>>>>> Error occurred:", e.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a function name to run.")
        sys.exit(1)
    
    function_name = sys.argv[1]
    if function_name == "run":
        run()
    else:
        print(f"Function {function_name} not found.")