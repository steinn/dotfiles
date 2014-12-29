if [ $UID -eq 0 ]; then NCOLOR="red"; else NCOLOR="yellow"; fi

function virtualenv_prompt_info
{
    if ! [ $VIRTUAL_ENV ]; then
        return
    fi
    local venv=$(basename $VIRTUAL_ENV)
    echo "venv:$venv"
}

PROMPT='%{$fg[$NCOLOR]%}%c ➤ %{$reset_color%}'
RPROMPT='%{$fg[$NCOLOR]%} $(git_prompt_info) $(virtualenv_prompt_info) [%*]%{$reset_color%}'

ZSH_THEME_GIT_PROMPT_PREFIX="git:"
ZSH_THEME_GIT_PROMPT_SUFFIX=""
ZSH_THEME_GIT_PROMPT_DIRTY="*"
ZSH_THEME_GIT_PROMPT_CLEAN=""
