# 42-RetrieveTime #

## Introduction ##

42-RetrieveTime permet de récupérer le temps total passé à l'école.

*L'outil utilise la V2 de 42, s'il y a eu des changements de comportement ou des modifications des accès à certaines données, il est possible que ça ne fonctionne plus.*

## Comment utiliser 42-RetrieveTime ? ##

```sh
./time.sh <month>
./time.sh <month> <length>
./time.sh <username> <month> <length>
OPTIONS :
        [length] is short or full, short by default
        [month] should be between 1 and 12, current by default
        [username] is your username given on your intra
```

Exemple pour : `./time.sh username 5 full`

```txt
Début: 2025-05-31 08:09:43.407000, Fin: 2025-05-31 12:14:43.384000, Durée: 4:04:59.977000
...
Début: 2025-05-17 13:19:43.277000, Fin: 2025-05-17 13:35:43.230000, Durée: 0:15:59.953000
Temps total passé en 05/12 : 152h 40min
```

## Comment paramétrer 42-RetrieveTime ? ##

Pour utiliser 42-RetrieveTime, il faut :

* créer une nouvelle application sur l'outil de gestions des API de 42
* créer un fichier .env comme suit :

.env file

```txt
CLIENT_ID=u-s4t2ud-9...
CLIENT_SECRET=s-s4t2ud-e...
```

Le programme rajoutera la variable 'auth_token' automatiquement dès qu'on exécute le script.

Le fichier ressemblera à quelque chose comme ça :

```txt
CLIENT_ID=u-s4t2ud-924bf38143ee926e6ef925ef245s34f462f621d433205f21s740a224190f34e
CLIENT_SECRET=s-s4t2ud-e234d91d71f90479dw07b815404864w689f8fffwa19dc6cb4o1o9c68361aa5
auth_token='814563a9e5737bfdc6cb4o1o9c683495277ecc396b57944122d5316f1d8d51a6'
```

Le fichier est déchiffré pour l'exécution du programme puis rechiffré à la fin de celui-ci.

Le chiffrement se fait à l'aide d'une clé, contenue dans le fichier .key, qui elle aussi est créée automatiquement au premier démarrage.
