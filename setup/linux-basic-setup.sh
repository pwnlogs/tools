echo 'updating and upgrading'
sudo apt update
sudo apt upgrade

echo 'installing vim'
sudo apt install vim
echo 'configuring vim'
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

sudo bash -c 'cat > /root/.vimrc <<EOL
filetype plugin indent on
set tabstop=4
set shiftwidth=4
set expandtab
set number
syntax on
set showcmd
set clipboard=unnamedplus
set autoindent
EOL'

echo 'add alias for vim'
echo 'alias vi=vim' >> ~/.bashrc

echo 'install tree'
sudo apt install tree

echo 'install wget'
sudo apt install wget

echo 'install snap'
sudo apt install snapd

echo 'install sqllite browser'
snap install sqlitebrowser
