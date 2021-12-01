# copy VPN IP to clipboard (IP of tun0 interface)
alias cpvpnip="ifconfig | tr '\n' '#' | sed 's/##/\n/g' | grep tun0 | sed -r 's/\s{4,}/\n/g' | grep 'inet ' | cut -d ' ' -f2 | xclip"

# print VPN IP to stdout (IP of tun0 interface)
alias vpnip="ifconfig | tr '\n' '#' | sed 's/##/\n/g' | grep tun0 | sed -r 's/\s{4,}/\n/g' | grep 'inet ' | cut -d ' ' -f2"

# toggle http(s) proxy to 127.0.0.1:8080 
alias proxy_switch='[[ -z "${http_proxy}" ]] && { export http_proxy=127.0.0.1:8080; export https_proxy=127.0.0.1:8080; echo -e "\033[0;32m Burp proxy turned on \033[0m"; } || { unset http_proxy; unset https_proxy; echo -e "\033[0;31m proxy turned off \033[0m"; }'

# add shortcut for `ls -la`
alias l='ls -la'

# set proxy to 127.0.0.1:<port-number>
# usage: set_proxy <port-number>
set_proxy(){
    export http_proxy="http://127.0.0.1:$1/"
    export https_proxy="http://127.0.0.1:$1/"
}

# locate a file and copy to the current directory. copies only the first match (the file-name is expected to be unique).
# usage: locate_n_cp <file-name>
locate_n_cp(){
    cp $(locate $1) $(echo $1 | rev | cut -d'/' -f1 | rev)
}

# colored prompt
PS1='${debian_chroot:+($debian_chroot)}\[\033[01;35m\]\u\[\033[01;30m\]@\[\033[01;32m\]\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n\$ '
