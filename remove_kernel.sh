#!/bin/bash

# Script to remove a custom built kernel installed from source
# Usage: sudo ./remove-kernel.sh <kernel-version>

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Check for correct usage
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <kernel-version>"
    exit 1
fi

VERSION=$1

# Define the paths and file patterns
BOOT_PATH="/boot"
MODULE_PATH="/lib/modules"
KERNEL_HEADERS="/usr/src"
KERNEL_FILES=("vmlinuz-$VERSION" "initrd.img-$VERSION" "config-$VERSION" "System.map-$VERSION")

# Remove kernel files from /boot
echo "Removing kernel files from $BOOT_PATH..."
for FILE in "${KERNEL_FILES[@]}"; do
    if [ -e "$BOOT_PATH/$FILE" ]; then
        echo "Removing $BOOT_PATH/$FILE"
        rm "$BOOT_PATH/$FILE"
    else
        echo "File not found: $BOOT_PATH/$FILE"
    fi
done

# Remove modules directory
echo "Removing modules directory from $MODULE_PATH/$VERSION..."
if [ -d "$MODULE_PATH/$VERSION" ]; then
    rm -r "$MODULE_PATH/$VERSION"
    echo "Removed $MODULE_PATH/$VERSION"
else
    echo "Directory not found: $MODULE_PATH/$VERSION"
fi

# Remove modules directory
echo "Removing kernel headers directory from $KERNEL_HEADERS/linux-headers-$VERSION..."
if [ -d "$KERNEL_HEADERS/linux-headers-$VERSION" ]; then
    rm -r "$KERNEL_HEADERS/linux-headers-$VERSION"
    echo "Removed $KERNEL_HEADERS/linux-headers-$VERSION"
else
    echo "Directory not found: $KERNEL_HEADERS/linux-headers-$VERSION"
fi

# Update GRUB
echo "Updating GRUB configuration..."
#update-grub

echo "Kernel version $VERSION removed successfully."

