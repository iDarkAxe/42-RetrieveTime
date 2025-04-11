#!/bin/bash

ALT_MESSAGE1="./time.sh <month>"
ALT_MESSAGE2="./time.sh <month> <length>"
ALT_MESSAGE3="./time.sh <username> <month> <length>"
ALT="$ALT_MESSAGE1\n$ALT_MESSAGE2\n$ALT_MESSAGE3"
OPTIONNAL="OPTIONNAL :"
LENGTH_MESSAGE="\t[length] is short or full, short by default"
MONTH_MESSAGE="\t[month] should be between 1 and 12, current by default"
USERNAME_MESSAGE="\t[username] is your username given on your intra"
OPT="$OPTIONNAL\n$LENGTH_MESSAGE\n$MONTH_MESSAGE\n$USERNAME_MESSAGE"
MESSAGE="$ALT\n$OPT"

DEFAULT_USER="ppontet"
DEFAULT_SIZE="0"

. ./fx.sh

if [[ $1 == "24" ]]; then
    rm -rf token.json
    python3 ./retrieve_token.py
    exit 1
fi
if [[ "$#" == "0" ]]; then
    echo -e $MESSAGE
    exit 1
elif [[ "$#" == "1" ]]; then
    defMonth $1
    USER="$DEFAULT_USER"
    SIZE="$DEFAULT_SIZE"
elif [[ "$#" == "2" ]]; then
    defMonth $1
    defSize $2
    USER="$DEFAULT_USER"
elif [[ "$#" == "3" ]]; then
    defUsername $1
    defMonth $2
    defSize $3
fi

# printInfos
# printMoreInfos

if [[ "$#" == "1" || "$#" == "2" || "$#" == "3" ]]; then
    python3 ./42_time.py $USER $SIZE $MONTH
    if [[ "$?" != 0 ]]; then
        python3 ./retrieve_token.py
        python3 ./42_time.py $USER $SIZE $MONTH
        if [[ "$?" != 0 ]]; then
            echo -e "Stopping here as it crashed already one time"
    fi
    fi
fi
exit 0
