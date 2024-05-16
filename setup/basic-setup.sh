echo '>>> updating and upgrading'
sudo apt -y update
sudo apt -y upgrade
echo '<<< update and upgrade done'

# custom folders
mkdir ~/apps
mkdir ~/configs
mkdir ~/projects

# tools
echo '>>> vim setup'
sudo apt install -y vim
cat > ~/.vimrc <<EOL
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab
set number
syntax on
set showcmd
set clipboard=unnamedplus
set autoindent
EOL
sudo cp ~/.vimrc /root/.vimrc
echo 'alias vi=vim' >> ~/.bashrc
echo '<<< vim setup done'

# tools
echo '>>> installing essential tools'
sudo apt install -y curl
sudo apt install -y tree
sudo apt install -y wget
sudo apt install python3-pip
sudo apt install git
sudo apt install tmux
wget -O ~/.tmux.conf 'https://raw.githubusercontent.com/pwnlogs/tools/main/setup/.tmux.conf'
sudo cp ~/.tmux.conf /root/.tmux.conf
# setup tmux plugins - https://github.com/tmux-plugins/tpm (tmux.conf updates are already made)
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
tmux source ~/.tmux.conf

# Graphic apps
sudo apt install terminator
# sudo apt install firefox
echo 'Please install the following manually:' 
echo '    - Google chrome'
echo '    - Visual studio code'
echo '    - Pycharm (community)'
echo '<<< installing essential tools done'

# bash additions
echo '>>> updating bashrc'
curl https://raw.githubusercontent.com/pwnlogs/tools/main/setup/bashrc-additions.sh >> ~/.bashrc
source ~/.bashrc
echo '<<< updating bashrc'
