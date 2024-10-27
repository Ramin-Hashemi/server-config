#########################
# File server_config.py #
#########################


import subprocess
import secret
import sys
import os


def wiki_server_config():
    install_packages()
    clone_github_repository()
    create_new_users()
    create_virtual_env()
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
    apt-get install -y virtualenv
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<install_packages>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<install_packages>>>>> Error occurred:", e.stderr)


def clone_github_repository():
    command = """
    su - root -c '
    sudo mkdir -p /home/web-apps &&
    cd /home/web-apps &&
    git clone https://Ramin-Hashemi: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@github.com/CognitiveLearn-Innovations/wiki.git
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
    su - root -c '
    # Create a new group
    groupadd --system ime-app-group &&
    # Create a new user, Add to the new group, Set the shell & home directory for the user
    useradd --system --gid ime-app-group --shell /bin/bash --home /home/web-apps ime-app-server-admin
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<create_new_users>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_new_users>>>>> Error occurred:", e.stderr)


def create_virtual_env():
    # Command to switch user, change directory, and activate virtual environment
    command = """
    su - ime-app-super-admin -c '
    cd /home/web-apps/wiki &&
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    pip install -r requirements.txt
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<create_virtual_env>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_virtual_env>>>>> Error occurred:", e.stderr)


def install_dependencies():
    # Install and build the required application dependencies
    command = """
    su - ime-app-super-admin -c '
    cd /home/web-apps/wiki &&
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    yarn install --frozen-lockfile &&
    yarn build
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<install_dependencies>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<install_dependencies>>>>> Error occurred:", e.stderr)


def create_database():
    # Command to switch user, change directory, and;
    # Create a new database  for the wiki
    command = """
    su - ime-app-super-admin -c '
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    # Create the database
    # yarn sequelize db:create &&

    # If you are not using SSL then use this command
    yarn sequelize db:create --env=production-ssl-disabled &&


    # Migrate the new database to add needed tables, indexes, etc
    # yarn sequelize db:migrate

    # If you are not using SSL then use this command
    yarn sequelize db:migrate --env=production-ssl-disabled
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<create_database>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<create_database>>>>> Error occurred:", e.stderr)


def start_app():
    command = """
    su - ime-app-super-admin -c '
    # Using virtualenv
    virtualenv . &&
    source bin/activate &&
    # Start the app
    yarn start
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<start_app>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<start_app>>>>> Error occurred:", e.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a function name to run.")
        sys.exit(1)
    
    function_name = sys.argv[1]
    if function_name == "wiki_server_config":
        wiki_server_config()
    else:
        print(f"Function {function_name} not found.")