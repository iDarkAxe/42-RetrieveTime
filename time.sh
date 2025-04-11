#!/bin/bash

MESSAGE="./time.sh [length] [month]\nOPTIONNAL :\n\t[length] is short or full, short by default\n\t[month] should be between 1 and 12, current by default"

# Vérifier si l'argument MONTH est passé (le premier argument)
if [[ ! -z $1 ]] && [[ ! "$1" =~ ^[0-9]+$ ]]; then
    echo "Erreur : Le mois doit être un nombre."
    echo -e $MESSAGE
    exit 1
fi

# Si un mois est spécifié, l'assigner à MONTH
if [[ ! -z $1 ]]; then
    MONTH=$1
else
    MONTH=""
fi

# Vérifier si un LENGTH est spécifié, sinon par défaut "short"
if [[ ! -z $2 ]]; then
    if [[ $2 == "short" ]]; then
        CHOICE="short"
    elif [[ $2 == "full" ]]; then
        CHOICE="full"
    else
        echo "Erreur : [length] doit être 'short' ou 'full'."
        echo -e $MESSAGE
        exit 1
    fi
else
    CHOICE="short"
fi

# Vérification du mois, s'il est spécifié
if [[ ! -z $MONTH ]]; then
    # Vérifier si le mois est entre 1 et 12
    if [[ "$MONTH" -lt 1 ]] || [[ "$MONTH" -gt 12 ]]; then
        echo "Erreur : Le mois doit être un nombre entre 1 et 12."
        echo -e $MESSAGE
        exit 1
    fi
fi

# Affichage de ce qui a été choisi
# echo "Mois choisi : $MONTH, Taille choisie : $CHOICE"

if [[ $CHOICE == "short" ]]; then
    python3 ./42_time.py $USER 0 $MONTH
elif [[ $CHOICE == "full" ]]; then
    python3 ./42_time.py $USER 1 $MONTH
else
    echo "Error AT CHOICE ??"
fi
