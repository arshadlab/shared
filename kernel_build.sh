#Optional
scripts/config --disable SYSTEM_TRUSTED_KEYS
scripts/config --disable SYSTEM_REVOCATION_KEYS

# May add CONFIG_DEBUG_INFO=n to .config to improve compile time but will unable to trace back on Oops using gdb
# Below enabling back.
scripts/config --set-val GDB_SCRIPTS y
scripts/config --set-val DEBUG_INFO y
scripts/config --undefine DEBUG_INFO_SPLIT
scripts/config  --set-val DEBUG_INFO_REDUCED y
scripts/config --set-val  DEBUG_INFO_NONE       n
scripts/config --set-val  DEBUG_INFO_DWARF5     y

yes ""  | make oldconfig



#Method 1
make -j $(nproc) INSTALL_MOD_STRIP=1 
make-kpkg --rootcmd=fakeroot --initrd --uc --us -j2 kernel_image 

#Method 2
# May have to delete vmlinux-gdb.py at root otherwise create problem
make -j$(nproc)  INSTALL_MOD_STRIP=1 deb-pkg
sudo dpkg -i ../linux-image-6.x.0_xxxx_amd64.deb 
sudo update-grub

