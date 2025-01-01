#/usr/bin/bash

#!/bin/bash

KERNEL_DIR=./linux_git/
cd $KERNEL_DIR

# Check if the first command line argument is provided
if [ -n "$1" ]; then
    LOCALVERSION=$1
else
    LOCALVERSION=-custom
fi

KERNEL_VERSION=$(make kernelrelease LOCALVERSION=$LOCALVERSION)
KERNEL_VERSION_NO_VER=$(make kernelrelease LOCALVERSION=)

#echo $KERNEL_VERSION
rm ../*${KERNEL_VERSION}*
time make -j$(nproc) INSTALL_MOD_STRIP=1 bindeb-pkg LOCALVERSION=$LOCALVERSION

cd ..
sudo dpkg -i linux-headers-${KERNEL_VERSION}_*.deb
sudo dpkg -i linux-image-${KERNEL_VERSION}_*.deb
sudo dpkg -i linux-image-${KERNEL_VERSION}-dbg_*.deb
sudo dpkg -i linux-libc-dev_${KERNEL_VERSION_NO_VER}_*.deb
sudo cp ${KERNEL_DIR}/vmlinux /usr/src/linux-headers-${KERNEL_VERSION}/
