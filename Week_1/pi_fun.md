# Reset a the root password for a raspberry pi

Assuming you are running OSX with a Ubuntu VM (using VirtualBox).

# Step 1: Make the SD card accessible to your VM

OSX can't mount ext file systems, so we have to rely on our Ubuntu VM. Unfortunately, it is not so easy to give the VM access to the SD card. Here's how we do that.

First use `mount` to find the SD card. Here the card is `/dev/disk4` with `s1` suffix denoting the slice number.

```bash
$ mount
/dev/disk2 on / (hfs, local, journaled)
...
/dev/disk4s1 on /Volumes/boot (msdos, local, nodev, nosuid, noowners)
```

Next, use disk utility to unmount any mounted partitions. Now we need to make things play nice with VirtualBox:

```
# The path ~/VirtualBox\ VMs/ubuntu/sdcard.vmdk is up to you
sudo VBoxManage internalcommands createrawvmdk -filename ~/VirtualBox\ VMs/ubuntu/sdcard.vmdk -rawdisk /dev/disk4

sudo chmod 777 /dev/disk4
sudo chmod 777 VirtualBox\ VMs/ubuntu/sdcard.vmdk
```

Finally, you need to use the Virtualbox GUI to add the raw vmdk file as a hard disk. If you get errors, make sure OSX didn't get sneaky and remount the SD card.

More detailed instructions [here](https://www.geekytidbits.com/mount-sd-card-virtualbox-from-mac-osx/).

# Step 2: Mount the card in your VM

This step is straight-forward:

```bash
#find the raw disk
sudo fdisk -l 
...
mkdir /tmp/mountpoint/
mount /dev/sdb2 /tmp/mountpoint/
```

# Step 3 Reset the Password

The [usual way](https://www.howtogeek.com/howto/linux/reset-your-ubuntu-password-easily-from-the-live-cd/) to do this would be to use `chroot` and `passwd`. Unfortunately, this technique won't work because the VM is x86 and the Rasbian binaries are all ARM, i.e., `chroot` gives an execution error when it tries to launch the shell. Instead, we need to directly modify the /tmp/mountpoint/etc/passwd and shadow files. Make sure to `sudo vi` (or use `chown`).

For the passwd file, find the line for root and remove the `x` from the second column, i.e., `:x:` becomes `::`. For the shadow file, delete all of the columns to make it look something like this: `root::::`.

More detailed instructions [here](https://www.novell.com/coolsolutions/trench/15629.html).
