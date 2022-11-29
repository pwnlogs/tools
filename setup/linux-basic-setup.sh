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

echo 'add alias for vim'
echo 'alias vi=vim' >> ~/.bashrc

echo 'install tree'
sudo apt install tree

echo 'install wget'
sudo apt install wget


# define aliases
cat > ~/.bashrc <<EOL
alias lxc-dev='lxc exec dev -- sudo --user ubuntu --login bash'
alias l='ls -la'
alias cpr='cp -r -u'
alias nmap='sudo nmap'
alias python=python3
alias comma-seperated='tr '\n' ',' | head -c -1'
EOL
echo '[TODO] Update lxc-dev alias
