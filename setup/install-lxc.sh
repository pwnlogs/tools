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
lxc image list ubuntu: 24.04 architecture=$(uname -m)
lxc launch ubuntu:24.04 dev # dev is the container name

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

