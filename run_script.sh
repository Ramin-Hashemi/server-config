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

# Run the Python script
if python3 server_config.py "run"; then
    echo "Python script executed successfully."
else
    echo "Failed to execute Python script." >&2
    exit 1
fi

# Keep the shell open
exec "$SHELL"