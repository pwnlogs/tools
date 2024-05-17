sudo apt update
sudo apt install snapd
sudo snap install lxd
# add current user to lxd group
getent group lxd | grep -qwF "$USER" || sudo usermod -aG lxd "$USER"
# logout and login or 
sudo su $USER
# init
lxd init --minimal

# Create a new container
lxc image list ubuntu: 24.04 architecture=$(uname -m) # look in ubuntu's repo
lxc image list images: 24.04 architecture=$(uname -m) # look at the default images repo
lxc launch ubuntu:24.04 dev # create using 24.04 image from ubuntu repo;  dev is the container name
lxc launch images:kali kali # create using kali image from 'images' repo; kali is the contianer name

# Allow emulation inside container
lxc config set dev security.nesting true
# Mark the container as privileged
lxc config set dev security.privileged true

# Allowing GUI apps on container
# allow root user (lxc is run as root) to impersonate user's UID ($UID, usually 1000)
echo "root:$UID:1" | sudo tee -a /etc/subuid /etc/subgid
# create GUI profile
lxc profile create gui-audio
curl https://raw.githubusercontent.com/pwnlogs/tools/main/setup/lxc-gui-audio-profile.yaml | lxc profile edit gui-audio
# apply profile to container
lxc profile add dev gui-audio
# NOTE: If there are errors about X0, check `ls /tmp/.X11-unix/` has X0 or X1 and update the profile accordingly
# Both the device path and the environment variable in the profile should be updated
# Install meso tools
lxc exec dev -- apt install -y mesa-utils
# Install pulse audio utils
lxc exec dev -- apt install -y pulseaudio-utils

# Share folders with the container
mkdir ~/lxc-share
lxc config device add dev share-lxc-share disk source=/home/$USER/lxc-share path=/home/ubuntu/lxc-share
mkdir ~/projects
lxc config device add dev share-projects disk source=/home/$USER/projects path=/home/ubuntu/projects

# Install apps
sudo apt install terminator
sudo snap install code --classic

# Graphic apps from sudo
xhost +
