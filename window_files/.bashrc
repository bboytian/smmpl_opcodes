# Alias definitions

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi


# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/c/Users/mpluser/Miniconda3/bin/conda.exe' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/c/Users/mpluser/Miniconda3/etc/profile.d/conda.sh" ]; then
        . "/c/Users/mpluser/Miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="/c/Users/mpluser/Miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

