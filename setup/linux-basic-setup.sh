echo '>>> updating and upgrading'
sudo apt -y update
sudo apt -y upgrade
echo '<<< update and upgrade done'

# tools
echo '>>> vim setup'
echo 'installing vim'
sudo apt install -y vim
echo 'configuring vim for user'
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
echo 'configuring vim for root'
sudo cp ~/.vimrc /root/.vimrc
echo 'add alias for vim'
echo 'alias vi=vim' >> ~/.bashrc
echo '<<< vim setup done'

# tools
echo '>>> installing essential tools'
echo 'install tree'
sudo apt install -y tree
echo 'install wget'
sudo apt install -y wget
echo '<<< installing essential tools done'
sudo apt install python3-pip

# aliases
echo '>>> defining aliases'
cat > ~/.bashrc <<EOL
alias lxc-dev='lxc exec dev -- sudo --user ubuntu --login bash'
alias l='ls -la'
alias cpr='cp -r -u'
alias nmap='sudo nmap'
alias python=python3
EOL
echo '[TODO] Update lxc-dev alias'
echo '<<< defining aliases done'

# functions
echo '>>> defining functions'
ports-from-nmap () { cat $1 | grep -E '/(tcp|udp)\s+open' | cut -d'/' -f1 | sort | uniq | tr '\n' ',' | head -c -1; }
echo '<<< defining functions done'
