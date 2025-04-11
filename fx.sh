#!/bin/bash

defMonth() {
	# Vérifier si l'argument MONTH est passé (le premier argument)
    if [[ ! -z $1 ]] && [[ ! "$1" =~ ^[0-9]+$ ]]; then
        echo "Erreur : Le mois doit être un nombre."
        echo -e $MESSAGE
        exit 1
    fi
    MONTH="$1"
    # Vérifier si le mois est entre 1 et 12
    if [[ "$MONTH" -lt 1 ]] || [[ "$MONTH" -gt 12 ]]; then
        echo "Erreur : Le mois doit être un nombre entre 1 et 12."
        echo -e $MESSAGE
        exit 1
    fi
}

defUsername() {
	USER="$1"
}

defSize() {
    if [[ $1 == "short" ]] || [[ $1 == "0" ]]; then
        SIZE="0"
    elif [[ $1 == "full" ]] || [[ $1 == "1" ]]; then
        SIZE="1"
    else
        echo "Erreur : [length] doit être 'short'(0) ou 'full'(1)."
        echo -e $MESSAGE
        exit 1
	fi
}

printInfos() {
    echo -e "Month\t:\t$MONTH"
    echo -e "User\t:\t$USER"
    echo -e "Size \t:\t$SIZE"
}

printMoreInfos() {
    python3 ./env_utils.py 2
}