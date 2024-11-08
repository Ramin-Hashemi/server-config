#!/usr/bin/env bash -x

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

# A best practices Bash script with many useful functions.
# This file configure the server from scratch to be fully prepared for iME projects.
# After the requirements and configurations set, this file will run all iME projects automatically.
# This script is meant to be entirely self-contained!

# Enable xtrace if the DEBUG environment variable is set
if [[ ${DEBUG-} =~ ^1|yes|true$ ]]; then
    set -o xtrace       # Trace the execution of the script (debug)
fi

# Only enable these shell behaviours if we're not being sourced
# Approach via: https://stackoverflow.com/a/28776166/8787985
if ! (return 0 2> /dev/null); then
    # A better class of script...
    set -o errexit      # Exit on most errors (see the manual)
    set -o nounset      # Disallow expansion of unset variables
    set -o pipefail     # Use last non-zero exit code in a pipeline
fi

# Enable errtrace or the error trap handler will not work as expected
set -o errtrace         # Ensure the error trap handler is inherited

# DESC: Handler for unexpected errors
# ARGS: $1 (optional): Exit code (defaults to 1)
# OUTS: None
# RETS: None
function script_trap_err() {
    local exit_code=1

    # Disable the error trap handler to prevent potential recursion
    trap - ERR

    # Consider any further errors non-fatal to ensure we run to completion
    set +o errexit
    set +o pipefail

    # Validate any provided exit code
    if [[ ${1-} =~ ^[0-9]+$ ]]; then
        exit_code="$1"
    fi

    # Output debug data if in Cron mode
    if [[ -n ${cron-} ]]; then
        # Restore original file output descriptors
        if [[ -n ${script_output-} ]]; then
            exec 1>&3 2>&4
        fi

        # Print basic debugging information
        printf '%b\n' "$ta_none"
        printf '***** Abnormal termination of script *****\n'
        printf 'Script Path:            %s\n' "$script_path"
        printf 'Script Parameters:      %s\n' "$script_params"
        printf 'Script Exit Code:       %s\n' "$exit_code"

        # Print the script log if we have it. It's possible we may not if we
        # failed before we even called cron_init(). This can happen if bad
        # parameters were passed to the script so we bailed out very early.
        if [[ -n ${script_output-} ]]; then
            # shellcheck disable=SC2312
            printf 'Script Output:\n\n%s' "$(cat "$script_output")"
        else
            printf 'Script Output:          None (failed before log init)\n'
        fi
    fi

    # Exit with failure status
    exit "$exit_code"
}

# DESC: Handler for exiting the script
# ARGS: None
# OUTS: None
# RETS: None
function script_trap_exit() {
    cd "$orig_cwd"

    # Remove Cron mode script log
    if [[ -n ${cron-} && -f ${script_output-} ]]; then
        rm "$script_output"
    fi

    # Remove script execution lock
    if [[ -d ${script_lock-} ]]; then
        rmdir "$script_lock"
    fi

    # Restore terminal colours
    printf '%b' "$ta_none"
}

# DESC: Exit script with the given message
# ARGS: $1 (required): Message to print on exit
#       $2 (optional): Exit code (defaults to 0)
# OUTS: None
# RETS: None
# NOTE: The convention used in this script for exit codes is:
#       0: Normal exit
#       1: Abnormal exit due to external error
#       2: Abnormal exit due to script error
function script_exit() {
    if [[ $# -eq 1 ]]; then
        printf '%s\n' "$1"
        exit 0
    fi

    if [[ ${2-} =~ ^[0-9]+$ ]]; then
        printf '%b\n' "$1"
        # If we've been provided a non-zero exit code run the error trap
        if [[ $2 -ne 0 ]]; then
            script_trap_err "$2"
        else
            exit 0
        fi
    fi

    script_exit 'Missing required argument to script_exit()!' 2
}

# DESC: Generic script initialisation
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: $orig_cwd: The current working directory when the script was run
#       $script_path: The full path to the script
#       $script_dir: The directory path of the script
#       $script_name: The file name of the script
#       $script_params: The original parameters provided to the script
#       $ta_none: The ANSI control code to reset all text attributes
# RETS: None
# NOTE: $script_path only contains the path that was used to call the script
#       and will not resolve any symlinks which may be present in the path.
#       You can use a tool like realpath to obtain the "true" path. The same
#       caveat applies to both the $script_dir and $script_name variables.
# shellcheck disable=SC2034
function script_init() {
    # Useful variables
    readonly orig_cwd="$PWD"
    readonly script_params="$*"
    readonly script_path="${BASH_SOURCE[0]}"
    script_dir="$(dirname "$script_path")"
    script_name="$(basename "$script_path")"
    readonly script_dir script_name

    # Important to always set as we use it in the exit handler
    # shellcheck disable=SC2155
    readonly ta_none="$(tput sgr0 2> /dev/null || true)"
}

# DESC: Initialise colour variables
# ARGS: None
# OUTS: Read-only variables with ANSI control codes
# RETS: None
# NOTE: If --no-colour was set the variables will be empty. The output of the
#       $ta_none variable after each tput is redundant during normal execution,
#       but ensures the terminal output isn't mangled when running with xtrace.
# shellcheck disable=SC2034,SC2155
function colour_init() {
    if [[ -z ${no_colour-} ]]; then
        # Text attributes
        readonly ta_bold="$(tput bold 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly ta_uscore="$(tput smul 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly ta_blink="$(tput blink 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly ta_reverse="$(tput rev 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly ta_conceal="$(tput invis 2> /dev/null || true)"
        printf '%b' "$ta_none"

        # Foreground codes
        readonly fg_black="$(tput setaf 0 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly fg_blue="$(tput setaf 4 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly fg_cyan="$(tput setaf 6 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly fg_green="$(tput setaf 2 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly fg_magenta="$(tput setaf 5 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly fg_red="$(tput setaf 1 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly fg_white="$(tput setaf 7 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly fg_yellow="$(tput setaf 3 2> /dev/null || true)"
        printf '%b' "$ta_none"

        # Background codes
        readonly bg_black="$(tput setab 0 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly bg_blue="$(tput setab 4 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly bg_cyan="$(tput setab 6 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly bg_green="$(tput setab 2 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly bg_magenta="$(tput setab 5 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly bg_red="$(tput setab 1 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly bg_white="$(tput setab 7 2> /dev/null || true)"
        printf '%b' "$ta_none"
        readonly bg_yellow="$(tput setab 3 2> /dev/null || true)"
        printf '%b' "$ta_none"
    else
        # Text attributes
        readonly ta_bold=''
        readonly ta_uscore=''
        readonly ta_blink=''
        readonly ta_reverse=''
        readonly ta_conceal=''

        # Foreground codes
        readonly fg_black=''
        readonly fg_blue=''
        readonly fg_cyan=''
        readonly fg_green=''
        readonly fg_magenta=''
        readonly fg_red=''
        readonly fg_white=''
        readonly fg_yellow=''

        # Background codes
        readonly bg_black=''
        readonly bg_blue=''
        readonly bg_cyan=''
        readonly bg_green=''
        readonly bg_magenta=''
        readonly bg_red=''
        readonly bg_white=''
        readonly bg_yellow=''
    fi
}

# DESC: Initialise Cron mode
# ARGS: None
# OUTS: $script_output: Path to the file stdout & stderr was redirected to
# RETS: None
function cron_init() {
    if [[ -n ${cron-} ]]; then
        # Redirect all output to a temporary file
        script_output="$(mktemp --tmpdir "$script_name".XXXXX)"
        readonly script_output
        exec 3>&1 4>&2 1> "$script_output" 2>&1
    fi
}

# DESC: Acquire script lock
# ARGS: $1 (optional): Scope of script execution lock (system or user)
# OUTS: $script_lock: Path to the directory indicating we have the script lock
# RETS: None
# NOTE: This lock implementation is extremely simple but should be reliable
#       across all platforms. It does *not* support locking a script with
#       symlinks or multiple hardlinks as there's no portable way of doing so.
#       If the lock was acquired it's automatically released on script exit.
function lock_init() {
    local lock_dir
    if [[ $1 = 'system' ]]; then
        lock_dir="/tmp/$script_name.lock"
    elif [[ $1 = 'user' ]]; then
        lock_dir="/tmp/$script_name.$UID.lock"
    else
        script_exit 'Missing or invalid argument to lock_init()!' 2
    fi

    if mkdir "$lock_dir" 2> /dev/null; then
        readonly script_lock="$lock_dir"
        verbose_print "Acquired script lock: $script_lock"
    else
        script_exit "Unable to acquire script lock: $lock_dir" 1
    fi
}

# DESC: Pretty print the provided string
# ARGS: $1 (required): Message to print (defaults to a green foreground)
#       $2 (optional): Colour to print the message with. This can be an ANSI
#                      escape code or one of the prepopulated colour variables.
#       $3 (optional): Set to any value to not append a new line to the message
# OUTS: None
# RETS: None
function pretty_print() {
    if [[ $# -lt 1 ]]; then
        script_exit 'Missing required argument to pretty_print()!' 2
    fi

    if [[ -z ${no_colour-} ]]; then
        if [[ -n ${2-} ]]; then
            printf '%b' "$2"
        else
            printf '%b' "$fg_green"
        fi
    fi

    # Print message & reset text attributes
    if [[ -n ${3-} ]]; then
        printf '%s%b' "$1" "$ta_none"
    else
        printf '%s%b\n' "$1" "$ta_none"
    fi
}

# DESC: Only pretty_print() the provided string if verbose mode is enabled
# ARGS: $@ (required): Passed through to pretty_print() function
# OUTS: None
# RETS: None
function verbose_print() {
    if [[ -n ${verbose-} ]]; then
        pretty_print "$@"
    fi
}

# DESC: Combines two path variables and removes any duplicates
# ARGS: $1 (required): Path(s) to join with the second argument
#       $2 (optional): Path(s) to join with the first argument
# OUTS: $build_path: The constructed path
# RETS: None
# NOTE: Heavily inspired by: https://unix.stackexchange.com/a/40973
function build_path() {
    if [[ $# -lt 1 ]]; then
        script_exit 'Missing required argument to build_path()!' 2
    fi

    local new_path path_entry temp_path

    temp_path="$1:"
    if [[ -n ${2-} ]]; then
        temp_path="$temp_path$2:"
    fi

    new_path=
    while [[ -n $temp_path ]]; do
        path_entry="${temp_path%%:*}"
        case "$new_path:" in
            *:"$path_entry":*) ;;
            *)
                new_path="$new_path:$path_entry"
                ;;
        esac
        temp_path="${temp_path#*:}"
    done

    # shellcheck disable=SC2034
    build_path="${new_path#:}"
}

# DESC: Check a binary exists in the search path
# ARGS: $1 (required): Name of the binary to test for existence
#       $2 (optional): Set to any value to treat failure as a fatal error
# OUTS: None
# RETS: 0 (true) if dependency was found, otherwise 1 (false) if failure is not
#       being treated as a fatal error.
function check_binary() {
    if [[ $# -lt 1 ]]; then
        script_exit 'Missing required argument to check_binary()!' 2
    fi

    if ! command -v "$1" > /dev/null 2>&1; then
        if [[ -n ${2-} ]]; then
            script_exit "Missing dependency: Couldn't locate $1." 1
        else
            verbose_print "Missing dependency: $1" "${fg_red-}"
            return 1
        fi
    fi

    verbose_print "Found dependency: $1"
    return 0
}

# DESC: Validate we have superuser access as root (via sudo if requested)
# ARGS: $1 (optional): Set to any value to not attempt root access via sudo
# OUTS: None
# RETS: 0 (true) if superuser credentials were acquired, otherwise 1 (false)
function check_superuser() {
    local superuser
    if [[ $EUID -eq 0 ]]; then
        superuser=true
    elif [[ -z ${1-} ]]; then
        # shellcheck disable=SC2310
        if check_binary sudo; then
            verbose_print 'Sudo: Updating cached credentials ...'
            if ! sudo -v; then
                verbose_print "Sudo: Couldn't acquire credentials ..." \
                    "${fg_red-}"
            else
                local test_euid
                test_euid="$(sudo -H -- "$BASH" -c 'printf "%s" "$EUID"')"
                if [[ $test_euid -eq 0 ]]; then
                    superuser=true
                fi
            fi
        fi
    fi

    if [[ -z ${superuser-} ]]; then
        verbose_print 'Unable to acquire superuser credentials.' "${fg_red-}"
        return 1
    fi

    verbose_print 'Successfully acquired superuser credentials.'
    return 0
}

# DESC: Run the requested command as root (via sudo if requested)
# ARGS: $1 (optional): Set to zero to not attempt execution via sudo
#       $@ (required): Passed through for execution as root user
# OUTS: None
# RETS: None
function run_as_root() {
    if [[ $# -eq 0 ]]; then
        script_exit 'Missing required argument to run_as_root()!' 2
    fi

    if [[ ${1-} =~ ^0$ ]]; then
        local skip_sudo=true
        shift
    fi

    if [[ $EUID -eq 0 ]]; then
        "$@"
    elif [[ -z ${skip_sudo-} ]]; then
        sudo -H -- "$@"
    else
        script_exit "Unable to run requested command as root: $*" 1
    fi
}

# DESC: Usage help
# ARGS: None
# OUTS: None
# RETS: None
function script_usage() {
    cat << EOF
Usage:
     -h|--help                  Displays this help
     -v|--verbose               Displays verbose output
    -nc|--no-colour             Disables colour output
    -cr|--cron                  Run silently unless we encounter an error
EOF
}

# DESC: Parameter parser
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: Variables indicating command-line parameters and options
# RETS: None
function parse_params() {
    local param
    while [[ $# -gt 0 ]]; do
        param="$1"
        shift
        case $param in
            -h | --help)
                script_usage
                exit 0
                ;;
            -v | --verbose)
                verbose=true
                ;;
            -nc | --no-colour)
                no_colour=true
                ;;
            -cr | --cron)
                cron=true
                ;;
            *)
                script_exit "Invalid parameter was provided: $param" 1
                ;;
        esac
    done
}






# The trap command allows you to specify actions to be taken \
# when the script receives certain signals, such as SIGINT (Ctrl+C) or SIGTERM (termination signal).
# This can be useful for cleaning up resources or performing graceful shutdowns.
trap 'echo "Script interrupted!"; exit 1' SIGINT SIGTERM

# Load configuration
source /home/server-config/config.sh


# Function to run containers
run_containers() {
    echo "Starting containers..."
    docker-compose up -d
    # Add more container management steps
}

# Decrypt the secrets

USER=$(cat user.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
GROUP_NAME=$(cat group_name.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
SSH_KEY_PATH=$(cat ssh_key_path.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
PUBLIC_SSH_KEY=$(cat public_ssh_key.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
IP_ADDRESS=$(cat ip_address.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)

# Database
# mysql
MYSQL_DATABASE=$(cat mysql_database_name.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
MYSQL_USERNAME=$(cat mysql_database_username.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
MYSQL_PASSWORD=$(cat mysql_database_password.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
# postgres
POSTGRES_DATABASE=$(cat postgres_database_name.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
POSTGRES_USERNAME=$(cat postgres_database_username.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)
POSTGRES_PASSWORD=$(cat postgres_database_password.txt | openssl enc -aes-256-cbc -md sha512 -a -d -pbkdf2 -iter 100000 -salt -pass pass:encryption_key)

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

####################

# Monitoring Server

# Enable strict mode for better error handling
set -euo pipefail

# Server details
server_url="http://ime-agent.com"
email_recipient="ramin.hashemi@usa.com"

# Function to send email alerts
send_alert() {
  local message=$1
  echo "$message" | mail -s "Server Down Alert" "$email_recipient"
}

# Check server status
response=$(curl -s -o /dev/null -w "%{http_code}" "$server_url")

if [ "$response" -ne 200 ]; then
  send_alert "Server is down! HTTP status code: $response"
else
  echo "Server is up and running."
fi

####################

# Backup Server

# Enable strict mode for better error handling
set -euo pipefail

# Set the backup directory
backup_dir="/path/to/backup"

# Create the backup directory if it doesn't exist
mkdir -p "$backup_dir"

# List of files and directories to back up
backup_items=("/home/user/documents" "/etc" "/var/log")

# Timestamp for the backup file
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
backup_file="$backup_dir/backup_$timestamp.tar.gz"

# Function to log messages
log_message() {
  local message=$1
  echo "$(date +"%Y-%m-%d %H:%M:%S") - $message"
}

# Perform the backup
log_message "Starting backup..."
if tar -czf "$backup_file" "${backup_items[@]}"; then
  log_message "Backup complete: $backup_file"
else
  log_message "Backup failed!"
  exit 1
fi


# DESC: Main control flow
# ARGS: $@ (optional): Arguments provided to the script
# OUTS: None
# RETS: None
function main() {
    trap script_trap_err ERR
    trap script_trap_exit EXIT

    script_init "$@"
    parse_params "$@"
    cron_init
    colour_init
    #lock_init system
}

# Invoke main with args if not sourced
# Approach via: https://stackoverflow.com/a/28776166/8787985
if ! (return 0 2> /dev/null); then
    main "$@"
fi

# vim: syntax=sh cc=80 tw=79 ts=4 sw=4 sts=4 et sr