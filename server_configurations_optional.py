########################
# File serverConfig.py #
########################


import subprocess
import secret
import sys
import os


def ime_app_server_configurations():
    unattended_upgrades()


def unattended_upgrades():
    # Configure unattended-upgrades to run automatically
    command = """
    su - root -c '
    echo "APT::Periodic::Update-Package-Lists \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades
    echo "APT::Periodic::Unattended-Upgrade \\"1\\";" >> /etc/apt/apt.conf.d/20auto-upgrades
    echo "APT::Periodic::AutocleanInterval \\"7\\";" >> /etc/apt/apt.conf.d/20auto-upgrades
    '
    """
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, executable='/bin/bash', check=True, capture_output=True, text=True)
        print("<unattended_upgrades>>>>> Function executed successfully:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("<unattended_upgrades>>>>> Error occurred:", e.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a function name to run.")
        sys.exit(1)
    
    function_name = sys.argv[1]
    if function_name == "ime_app_server_configurations":
        ime_app_server_configurations()
    else:
        print(f"Function {function_name} not found.")