
# >>> >>> >>> BASH ADDITIONS

# >>> aliases
alias l='ls -la'
alias vi='vim'
alias python='python3'
alias nmap='sudo nmap'
alias cpr='cp -r -u'
alias xclip='xclip -selection c'
alias lxc-dev='lxc exec dev -- sudo --user ubuntu --login bash'
# <<< aliases

# >>> defining functions
ports-from-nmap () { cat $1 | grep -E '/(tcp|udp)\s+open' | cut -d'/' -f1 | sort | uniq | tr '\n' ',' | head -c -1; }
mkdir-and-cd () { mkdir $1; cd $1; }
# <<< defining functions done

# >>> define $PS1
export PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n\$ '
# <<< define $PS1

# <<< <<< <<< BASH ADDITIONS
