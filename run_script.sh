#!/bin/bash

import secret

# Install dpkg
if sudo dpkg --configure -a; then
    echo "dpkg installed successfully."
else
    echo "Failed to install dpkg." >&2
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
    sudo apt-get install -y python3-venv
    sudo apt-get install -y build-essential
    sudo apt-get install -y ubuntu-gnome-desktop gnome-terminal gnome-browser-connector
    echo "Packages installed successfully."
else
    echo "Failed to install packages." >&2
    exit 1
fi

# Keep the shell open
exec "$SHELL"