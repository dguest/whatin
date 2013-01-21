# bash completion function for whatin routine 
# Author: Dan Guest <dguest@cern.ch>
# Fri Jun  8 11:04:41 CEST 2012

_whatin() 
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="-e --help"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    elif [[ ${prev} == -e ]] ; then
	# some hacks because athena sets LD_LIBRARY_PATH
	if [[ -n $ATLAS_POOLCOND_PATH ]] ; then 
	    old_ld=$LD_LIBRARY_PATH
	    unset LD_LIBRARY_PATH
	fi
	# need to pipe root errors to /dev/null
	WORDS=$(auto-complete-root.py ${COMP_WORDS[1]} ${cur} 2>/dev/null ) 
        COMPREPLY=( $(compgen -W "${WORDS}" -- ${cur}) )
	if [[ -n $old_ld ]] ; then 
	    export LD_LIBRARY_PATH=$old_ld
	fi 
        return 0
    else 
        COMPREPLY=( $(compgen -o plusdirs -f -X "!*.root*" -- ${cur}) )
	return 0
    fi
}

alias whatin=whatin.py
complete -o filenames -o nospace -F _whatin whatin
