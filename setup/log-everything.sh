# >>>> log everything
if [ -z "$UNDER_SCRIPT" ]; then
    logdir=$HOME/conlogs
    if [ ! -d $logdir ]; then
        mkdir $logdir
    fi  
    logfile=$logdir/$(date +%F_%T).$$.log
    export UNDER_SCRIPT=$logfile
    script -f -q $logfile
    exit
fi
# <<<< log everything
# Note: if you change directory after script command,
#       cd will happen in the script environment
#       but if you split the window afterwards in Terminator,
#       the new window will be started from
#       working directory of the original environment and not the script environment 
