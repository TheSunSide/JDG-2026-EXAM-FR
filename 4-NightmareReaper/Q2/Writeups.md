# Alterations

En utilisant le site web Stegonline, avec l'outil "browse bitplanes", on trouve du noise dans les couches RGB 0 et 1, ce qui donne l'indice que les LSB ont étés manipulés. Avec Apérisolve (https://www.aperisolve.com/), nous avons accès à plusieurs outils de stéganographie. Dans la section zsteg, nous avons le flag qui aparait: FLAG-M3RC1_3V1D3NT

# InYourDreams

Pour ce fichier, j'ai utilisé l'outil steghide, qui permet de cacher ou d'extraire des données cachées d'un fichier. Sans passphrase, j'ai extrait dans hidden.txt le flag: FLAG-L4_R34LIT3_N3TFL1X

# Whats-This

Pour ce fichier, j'ai commencé par utilisé l'outil exiftool, qui mentionne qu'il s'agit d'un fichier zip. J'ai ensuite utilisé la commande `binwalk -Me` pour extraire récursivement le contenu du fichier. Cela à donné le fichier hidden.txt qui contient le flag: FLAG-F1ND1NG_A_F1L3 