**1. Algorithmes (Pseudocode)**

**Structure de base**

DÉBUT

Instructions.

FIN.

**Lecture & écriture**

* LIRE Variable. → reçoit une donnée (clavier, capteur, port).
* ÉCRIRE Variable. → affiche la valeur d’une variable.
* ÉCRIRE "Texte". → affiche un texte.

**Affectation (=)**

* X = 10. → assigne une valeur.
* Y = (X\*9)/5+32. → opérations avec priorité et parenthèses.

**Décision**

SI (Condition)

Instructions

SINON

Instructions

FIN SI.

**Boucle**

TANT QUE (Condition)

Instructions

FIN TANT QUE.

La condition doit finir par devenir FAUSSE → sinon boucle infinie.

**Opérateurs logiques**

* ET (&& en C) → les deux conditions vraies
* OU (|| en C) → au moins une condition vraie
* NON (! en C) → inverse la condition
* == égal, != différent, <, >, <=, >= comparaisons

**2. Types de données**

* **Nombre** : ex. Surface = 8\*7.
* **Caractère** : 'A', '1'.
* **Chaîne de caractères** : "Bonjour".

**3. Introduction au langage C**

**Structure minimale**

int main(void) {

// instructions

}

**Équivalences Algo → C**

* SI → if(...) { ... } else { ... }
* TANT QUE → while(...) { ... }
* ÉCRIRE → printf(...)
* LIRE → getchar()

**Entrées / sorties**

* getchar() → lit une touche (ASCII).
* printf() → affiche à l’écran.

**Formats principaux :**

* %d entier
* %f flottant
* %c caractère
* %s chaîne
* %x / %X hexadécimal

**4. Bases numériques**

* **Binaire** : baste 2 (0 et 1).
* **Décimal → Binaire** : divisions successives.
* **Binaire → Décimal** : somme des puissances de 2.
* **Hexadécimal** : regroupe les bits par 4. Ex: 0xB5C.

**5. Opérations sur bits**

* & (ET) → met des bits à 0.
* | (OU) → met des bits à 1.
* ^ (OU Exclusif) → inverse des bits.
* **Masque** : utilisé pour isoler certains bits.

**6. Microcontrôleurs & Ports**

* Lecture d’un port : ucReadPort(2);
* Écriture sur un port : vWritePort(valeur, port);
* Boutons → Pull-Up (2.2kΩ – 10kΩ) pour ramener à 1.
* LED souvent activée avec sortie 0 (sink).

**7. Structure avec Délai**

Boucle de délai pour ralentir un programme (ex. LED clignotante).
Exemple avec uiDelai = 1000; → attente d’1 seconde.

**8. Bonnes pratiques**

* Toujours **déclarer les variables** au début (int, float, char...).
* Utiliser des **commentaires** // ou /\* ... \*/.
* Pas d’accents dans le code.
* Convention : nom de variable = préfixe + majuscule (ex. iCompteur, fValeur).

**Résumé rapide**

1. Un **programme C** = fonction main() + instructions.
2. On lit avec getchar(), on écrit avec printf().
3. Les structures de contrôle : if, else, while.
4. Les **types** : int, float, char, unsigned.
5. Les **bases** : binaire, décimal, hexadécimal.
6. Les **ports** des microcontrôleurs se manipulent avec ucReadPort et vWritePort.
7. Toujours bien commenter, nommer et structurer le code.

**📖 Dictionnaire des codes C appris**

**Fonctions**

* int main(void) → fonction principale.
* getchar() → lit une touche clavier.
* printf("...") → affiche un message ou une variable.
* ucReadPort(x) → lit un port.
* vWritePort(val, port) → écrit sur un port.
* bReadPin(port, pin) → lit un bit précis.
* vWritePin(port, pin, val) → écrit sur un bit précis.

**Formats d’affichage (printf)**

* %d → entier signé (int)
* %u → entier non signé (unsigned int)
* %f → flottant
* %c → caractère
* %s → chaîne de caractères
* %x / %X → hexadécimal
* %% → affiche %

**Opérateurs**

* Arithmétiques : + - \* / %
* Affectation : =
* Comparaison : == != < > <= >=
* Logiques : && || !
* Bits : & | ^

**1. Définition d’une variable**

* Une **variable** est un espace en mémoire qui sert à **stocker une valeur** (nombre, caractère, texte, etc.).
* On peut changer son contenu au cours du programme.
* Exemple (pseudocode) :
* LIRE Distance.

Ici, Distance est la variable qui reçoit la valeur lue au clavier.

**2. Forme générale en C**

En C, on doit **déclarer** une variable avant de l’utiliser :

type nom;

* **type** : le genre de données (int, float, char, etc.).
* **nom** : le nom choisi pour la variable.

**3. Exemples de déclarations**

int age; // Nombre entier

float moyenne; // Nombre à virgule (réel)

char lettre; // Un seul caractère

On peut aussi **initialiser** (donner une valeur de départ) :

int iRayon = 2;

float fCirconf = 0.0;

 On ne peut pas utiliser scanf() ou getchar() directement dans la déclaration.

**4. Conventions de nommage**

* Doit commencer par une **lettre**.
* Peut contenir chiffres et lettres (ex. note1 est valide, 1note ne l’est pas).
* Sensible à la casse : Nom ≠ nom.
* Pas de mots réservés (if, else, while, etc.).
* Souvent on ajoute un **préfixe selon le type** :
  + i pour int → iCompteur
  + f pour float → fValeur
  + c pour char → cLettre

**5. Types de variables usuels**

| **Type** | **Taille (bits)** | **Exemple de valeurs** | **Format printf** |
| --- | --- | --- | --- |
| int | 16 ou 32 | -32768 à +32767 (ou plus) | %d |
| float | 32 | 3.14, -0.25, 1000.0 | %f |
| char | 8 | 'A', 'b', '7' | %c |
| unsigned int | 16 ou 32 | 0 à 65535 (positif) | %u |
| unsigned char | 8 | 0 à 255 | %c ou %u |

**6. Exemple complet**

#include <stdio.h>

int main(void) {

int longueur, largeur; // Déclaration

int superficie; // Déclaration

printf("Entrez la longueur : ");

scanf("%d", &longueur); // Lecture d’un entier

printf("Entrez la largeur : ");

scanf("%d", &largeur);

superficie = longueur \* largeur; // Utilisation

printf("La superficie est de %d\n", superficie);

return 0;

}

Float fcapteur