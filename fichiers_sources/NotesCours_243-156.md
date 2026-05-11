1. Analyse du problème

Avant de chercher une solution, il faut bien comprendre ce qui est demandé.

1.1 Identification du problème

Définir clairement la nature du problème.

Exemple : « Trier une liste de nombres du plus petit au plus grand ».

1.2 Identification des résultats désirés

Préciser l’objectif final attendu.

Exemple : « La liste doit être triée en ordre croissant ».

1.3 Identification des entrées nécessaires

Repérer toutes les données d’entrée.

Exemple : « La liste initiale de nombres ».

2. Résolution du problème

Une fois le problème bien compris, on cherche une solution sous forme d’algorithme.

2.1 Identification des étapes pour résoudre le problème (écrire l’algorithme)

Décomposer la solution en étapes logiques.

Exemple : « Comparer deux nombres, échanger si nécessaire, répéter jusqu’à ce que la liste soit triée ».

2.2 Vérification de la validité de l’algorithme (jeu d’essai)

Tester l’algorithme avec des exemples concrets.

Exemple : essayer avec [3, 1, 2] pour vérifier si le résultat final est [1, 2, 3].

2.3 Correction de l’algorithme

Si les tests échouent, revenir sur les étapes et corriger.

On répète le cycle 2.1 → 2.2 → 2.3 jusqu’à obtenir une solution correcte et fiable.

# 1. Introduction aux Algorithmes (Pseudocode)



Approche pour résoudre un problème simple.

Différence entre analogique et numérique :



## 1.1. La syntaxe:

### 1.1.1. DÉBUT / FIN:

Nos programmes commencent par DÉBUT et se termine par FIN.

Exemple (Pseudocode):

|  |  |
| --- | --- |
| DÉBUT |  |
| Instruction 1. | // Notez l'indentation de 3 espaces et le point |
| Instruction 2. | // terminal des instructions. |
| FIN. | // Notez le point à la fin du bloc |



Exemple avec POB: Les instructions **Début** et **Fin du programme**, sont accessible par le menu **Logique**.

Menu **Mouvements**.

Menu **Temps**

### 1.1.2. LIRE:

Instruction nous permettant de lire de l'information venant de l'extérieur du microprocesseur.

Par défaut (si rien n'est spécifié), l'information est lue au clavier. Exemple:

LIRE Distance. // Va lire le clavier et mémorise l'information dans

// "Distance".

// Notez le point. Toutes les instructions vont // se terminer par un point.

Distance: Nom représentant un espace dans lequel sera mémorisé de l'information.

C'est ce nom qui sera utilisé dans le reste du programme. Ça se nomme une **variable**.

Exemple avec POB:

Menu Capteurs


Permet de lire la distance (en mm) séparant un capteur et un obstacle.

La distance sera mémorisée dans la **variable** DistanceAvant, spécifiée dans le bloc

En pseudocode on écrirait: LIRE DistanceAvant au PORT1.


### 1.1.4. Affectation ( = ):

Permet de mettre le résultat d'une opération dans un contenant (variable).

Exemples:

TempC = 10. // Affecte la valeur 10 dans la variable TempC.

TemperatureF = ((TempC \* 9) / 5) + 32. // Ici il y a l'utilisation de plusieurs

// opérateurs de bases avant de faire

// l'affectation.

Explication: On prend le contenu de TempC (10), on multiplie par 9, ensuite on divise par 5 et finalement on additionne 32. Le résultat sera 50. Notez les parenthèses qui forcent l'exécution des opérateurs dans l'ordre cité.

Exemple avec POB:

Menu Mathématique

En pseudocode: Age = 12.

Autre exemple:

NBoucle = 23.

NBoucle = NBoucle + 1. // On augmente le contenu de NBoucle de 1.

Que contient NBoucle après l'exécution des 2 instructions? (**Notion importante**).

Exemple de calcul avec POB:

En pseudocode: Age = Age + 12.

Opérateurs disponible: **+**, **-**, **/**, **\*** et Reste de la division.



Menu Mathématique

Exemple de programme:

//////////////////////////////////////////////////////////////////

//

// Concepteur: Daniel Côté Date: 31/08/2010

//

// Description: Calcul la superficie d'un terrain en pieds carrés.

//

// En entrée: La longueur et la largeur sont entrées au clavier.

// En sortie: La superficie est affichée à l'écran.

//

//////////////////////////////////////////////////////////////////

DÉBUT

ÉCRIRE "Entrez la longueur du terrain".

LIRE Longueur.

ÉCRIRE "Entrez la largeur du terrain".

LIRE Largeur.

Superficie = Longueur \* Largeur.

ÉCRIRE "La superficie du terrain est de ". // Notez l'espace à la fin.

ÉCRIRE Superficie.

ÉCRIRE " pieds carrés". // Notez l'espace avant pieds.

FIN.

### 1.1.5. Décision ( Sélection binaire, Instruction de branchement ):

**SI** **(Condition)**

Instructions exécutées si "Condition" est vrai. **FIN SI**.

La condition est un test qui donne comme résultat VRAI ou FAUX. Si le test donne VRAI, les instructions sont exécutées. Si le test donne FAUX, on passe par-dessus les instructions et le programme se poursuit avec les instructions situées après le FIN SI.

Exemples:

|  |  |
| --- | --- |
| SI ( Temperature > 25 ) | // Notez l'opérateur de comparaison >. |
| Part le ventilateur. FIN SI. | // Met 1 à P1\_1. |

SI ( CapteurAvant == Actif ) // Notez l'égalité: ==. MoteurSensTourelle tourne à droite. // Met 1 à P3\_3.

|  |  |
| --- | --- |
| MoteurTourelle à ON. | // Met 0 à P3\_4. |
| MoteurChaineGauche à OFF. | // Met 1 à P3\_1. |
| MoteurChaineDroite à ON.  FIN SI.          **Exemple avec POB:** | // Met 0 à P3\_2. |

DEBUT



V



F

LIRE Distance au PORT1.

SI (Distance > 250)

Avancer.

FIN SI.

FIN.

Opérateurs disponibles avec POB: en C: Menu Logique

Supérieur à: > >

Supérieur ou égal à: >= >=

Inférieur à: < < Inférieur ou égal: <= <=

Égal: = ==

Différent: ! !=

### 1.1.6. Décision ( avec un bloc FAUX ):

**SI** **(Condition)**

Instructions si "Condition" est vrai. **SINON**

Instructions si "Condition" est faux.

|  |  |
| --- | --- |
| **FIN SI**.      Exemple: | // Fin du bloc. |
| SI ( Interrupteur == 1 ) Allume la lumière. | // Notez l'opérateur d'égalité ==. |
| SINON  Éteint la lumière.  FIN SI. | // Interrupteur à 0. |

**Exemple avec POB:**



V

F

DEBUT

LIRE Distance au PORT1.

SI (Distance > 250)

Avancer.

SINON

Tourner à gauche 90.

FIN SI.

FIN.

### 1.1.7. Boucle:

**TANT QUE** **(Condition)**

Instruction1.

Instruction2.

**FIN TANT QUE.** // Fin du bloc.

Exécute les instructions 1 et 2 tant que "Condition" est VRAI.

**Très important:** La condition doit devenir fausse à un certain moment, car sinon, on boucle à

l'infini.

Généralement, une instruction dans la boucle modifie la condition.

Exemple:

LIRE Touche. // Initialisation de Touche avant le test. TANT QUE (Touche != 'Q') // Notez le symbole différent de: **!=** . ÉCRIRE Touche. // 'Q': manière de représenter le code LIRE Touche. // de la lettre Q en langage C.

FIN TANT QUE.

**Exemple avec POB:**



V

F

DEBUT

LIRE Distance au PORT1.

TANT QUE(Distance > 250)

Avancer.

LIRE Distance au PORT1.

FIN TANT QUE.

FIN.

### 1.1.8. Opérateurs Logiques utilisés pour faire des tests (Condition):

== : Égalité. Vérifie si les deux membres sont identiques. Si c'est le cas, le résultat est VRAI.

SI( Hauteur == 12 )

!= : Différent de. Vérifie si les deux membres sont différents. Si c'est le cas le résultat est VRAI.

SI( Touche != 'Q')

ET : Ce mot relie deux conditions. Le résultat sera VRAI si les **deux** conditions sont VRAI. Autrement le résultat est FAUX.

SI((Temperature > 20) ET (Temperature < 40))

OU : Ce mot relie deux conditions. Le résultat sera VRAI si **une** des conditions est VRAI. Si les deux conditions sont fausses, le résultat est FAUX.

SI((Touche == 'a') OU (Touche == 'A'))

ÉCRIRE "On a pesé sur A".

FIN SI.

NON : Pour inverser une condition.

SI(NON(Touche == 'Q')) identique à SI(Touche != 'Q'))

Exemples:

SI( Heure > 17)

SI( Etat == 0)

SI((Valeur > 0) ET (Valeur < 10))

SI((Valeur <= 0) OU (Valeur >= 10))

LIRE Touche.

TANT QUE((Touche != 'Q') ET (Touche != 'q'))

Instructions.

LIRE Touche.

FIN TANT QUE.

### 1.1.9. Les opérateurs (résumé):

|  |  |
| --- | --- |
| - Calcul: | +, -, \*, /, % (modulo ou reste de la division (entier)) |
| - Affectation: | = |
| - Test: | <, >, ==, !=, <=, >=, ET, OU, NON |

Équivalent en C: && || !

Exercice:

Pour les tests suivants, dites si le résultat est **V**rai ou **F**aux.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  |  |  | # du Test | |  |
| Sw1 | Sw2 | 1 | 2 | 3 | 4 |
| 0 | 0 |  |  |  |  |
| 0 | 1 |  |  |  |  |
| 1 | 0 |  |  |  |  |
| 1 | 1 |  |  |  |  |

1. SI ((Sw1 == 1) ET (Sw2 == 1))
2. SI ((Sw1 == 1) OU (Sw2 == 1))
3. SI ((Sw1 == 0) OU (Sw2 == 0))

1. SI ((Sw1 == 0) ET (Sw2 == 0))

## 1.2. Évolution des fonctions de lecture et d'écriture:

### 1.2.1. LIRE:

Amène de l'information dans le CPU.

**LIRE Variable.** // Lecture au clavier. La donnée est mémorisée dans Variable.

**LIRE Variable à Adresse.** // Lire une donnée dans un circuit électronique

// situé à Adresse.

// La valeur lue est mémorisée dans Variable.

Exemple:

LIRE VitesseMoteur à 0x3B0. // 0x3B0 est l'adresse du circuit électronique

// où se trouve l'information (en hexadécimal).

// En Algo et en C on utilisera la notation **0x** // pour représenter les nombres hexadécimaux.

**LIRE Variable au Port.** // Lire une donnée (8 bits) sur les broches du CPU.

// La donnée est mémorisé dans Variable.

Exemple:

LIRE ConvTemp au Port1. // Le convertisseur pour la température est

// sur le port 1.

**LIRE Bit a P3\_2.** // Lire l'état **d'un** bit du CPU ( ici c'est le bit 2 du Port3).

Exemple:

LIRE BoutonStart à P1\_4. // Le bouton est sur le bit 4 du port 1.

### 1.2.2. ÉCRIRE:

Sort de l'information du CPU.

**ÉCRIRE Variable.** // Affiche à l'écran le contenu de Variable.

**ÉCRIRE "Message".** // Affiche à l'écran la suite de caractère "Message".

**ÉCRIRE Variable à Adresse.** // Écrit une donnée (contenue de Variable) dans

// un circuit électronique.

Exemple:

ÉCRIRE DelaiTimer à 0x3C4. // Le contenu de DelaiTimer est transmis

// à l'adresse 0x3C4.

**ÉCRIRE Variable au Port.** // Écrit une donnée 8 bits (contenue dans Variable) sur les

// broches du CPU.

Exemples:

ÉCRIRE VitesseMoteur au Port2. // Le contenu de VitesseMoteur est transmis

// au port2.

**ÉCRIRE EtatLed a P3\_5.** // Transmet la valeur de EtatLed (1 bit: 0 ou 1) sur le bit 5 du Port3.

**Problèmes:**

Voie ferré:



CapteurOuest

Route

CapteurEst



Lumière

1. Si un train croise un des capteurs, on allume la lumière. La longueur des trains est toujours plus grande que la distance entre les deux capteurs.
   * CapteurOuest est branché sur P3\_2. Si on lit 0, le capteur est actif.
   * CapteurEst est branché sur P3\_4. Si on lit 0, le capteur est actif.
   * Lumière est branchée sur P3\_5. Un 0 allume la lumière. Un 1 éteint la lumière.

Écrire l'algorithme:

Petite modification: On ajoute un capteur (P3\_3) sur le rail au milieu de la route. Ça nous permettra de détecter une condition erronée CapteurOuest **et** CapteurEst actif mais pas le nouveau. Dans ce cas on active une alarme (0 à P3\_6).

1. Suite de Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13, 21 …. Le dernier chiffre est la somme des deux précédents.

## 1.3. Types de données:

### 1.3.1. Nombre.

Un nombre représente une valeur numérique.

Exemple 1: Surface = 8 \* 7.

Exemple 2: LIRE Vitesse.

LIRE Temps.

Distance = Vitesse \* Temps.

### 1.3.2. Caractères.

Représente **le** caractère alphanumérique que nous voulons manipuler.

Exemple: LIRE Touche.

SI (Touche == 'Q')

Dans nos algorithmes et en langage C, l'utilisation des apostrophes signifie l'utilisation explicite du caractère alphanumérique.

Exemple: SI ( '1' > 1 ) // Explication:

### 1.3.3. Chaine de caractères.

Représente une suite de caractères que nous voulons manipuler comme une seule entité.

Exemple 1: ECRIRE "Message à l'écran". // L'utilisation des guillemets

// indique une chaine de // caractères alphanumériques.

Exemple 2: LIRE Nom. // La variable Nom, sert à identifier une chaine de // caractères. C'est le contexte qui nous permet de // savoir que c'est le type de donnée approprié.

En fonction du langage de programmation utilisé, des outils vont nous permettre de manipuler les différents types de données.

# 2. Introduction au langage C

En langage C, chaque algorithme sera transformé en fonction. Un programme est formé d'une ou de plusieurs fonctions. Il y a au moins une fonction obligatoire en C. C'est la fonction **main( )**.

Équivalence:

**Pseudocode**  **C**

//Principal int main(void)

DÉBUT {

// Instructions. // Instructions. // Instructions. // Instructions.

FIN. }

Un programme en C commence toujours par la première instruction à l'intérieur du main( ). Une fonction en C est reconnaissable à ces parenthèses à côté du nom.

Équivalence:

|  |  |  |
| --- | --- | --- |
| **Pseudocode** | **C** | |
| **SI( Test)** |  | **if(Test)** |
|  |  | **{** |
| // Instructions. |  | // Instructions. |
| // Instructions. |  | // Instructions. |
| **FIN SI.** |  | **}** |
| **SI( Temp < 28)** |  | **if(Temp < 28)** |
|  |  | **{** |
| // Instructions. |  | // Instructions. |
|  |  | **}** |
| **SINON** |  | **else** |
|  |  | **{** |
| // Instructions. |  | // Instructions. |
| **FIN SI.** |  | **}** |
| **TANT QUE(Touche != 'Q')** | | **while(Touche != 'Q')** |
|  | | **{** |
| // Instructions. | | // Instructions. |
| // Instructions. | | // Instructions. |
| **FIN TANT QUE.** | | **}** |

## 2.1. LIRE:

|  |  |
| --- | --- |
| **LIRE Touche.** | **Touche = getchar();** // Keil (stdio.h) |
| LIRE Nom. | // Pas d'équivalent pour l'instant. |
| LIRE Nombre | // Pas d'équivalent pour l'instant. |

La fonction getchar( ) fait partie de la définition de base du C. Elle est présente sur tous les compilateurs.

getchar( ): Attend qu'une touche soit pesée au clavier. Une fois la touche pesée, la fonction retourne le code ASCII de la touche et l'affiche à l'écran.

Code ASCII: Code numérique donné à chaque caractère afin de pouvoir le traiter dans les ordinateurs. Faites une recherche sur Internet avec "Table ASCII".

|  |  |  |
| --- | --- | --- |
| Code en Décimal | Code en Hexadécimal | Caractère |
| 10 | 0x0A | LF (Line Feed) |
| 13 | 0x0D | CR (Cariage Return) |
| 27 | 0x1B | Esc (escape) |
| 32 | 0x20 | Espace |
| 48-57 | 0x30 – 0x39 | '0' – '9' |
| 65 | 0x41 | 'A' |
| 97 | 0x61 | 'a' |

Certains caractères intéressant:

Exemple d'instruction en C: Clavier = getchar( );

Si je pèse sur la touche 'A' , que contient la variable Clavier? ( 'A' ou 0x41 ou 65 )

En fait c'est tout ça à la fois. Ça dépend de ce qu'on veut représenter. En TEP nous utiliserons surtout la valeur en hexadécimal (0x41) ou encore la représentation du caractère ('A').

Exemple:

**Pseudocode**  **C**

LIRE température. Temperature = getchar( );

Si je pèse sur **'1'** au clavier. Que contient Température?

Que doit-on faire si c'est la valeur numérique **1** qui m'intéresse?

##

## 2.2. Table ASCII -I



## 2.3. Table ASCII –II



## 2.4. ÉCRIRE:

|  |  |
| --- | --- |
| **Pseudocode** | **C** |
| ECRIRE "Message" | printf("Message"); // (stdio.h) |

La fonction printf( ) affiche à l'écran tout ce qui est entre les guillemets.

ECRIRE Température printf("%d", Temperature); // %d format d'affichage

// entier décimal. printf("%f", Temperature); // %f en point flottant.

L'utilisation du symbole %, permet d'afficher le contenu d'une variable avec le format voulu. Si on veut afficher % il faudra le mettre deux fois dans les guillemets ("%%").

### 2.4.1. Liste des principaux formats que vous utiliserez avec printf( )

|  |  |  |  |
| --- | --- | --- | --- |
| Format | Description: |  |  |
| %d | Nombre entier 16 bits (négatif ou positif). | %bd | 8 bits |
| %f | Nombre à point flottant. |  |  |
| %c | Caractère correspondant au numéro du code ASCII fournit. |  |  |
| %x | Nombre hexadécimal (lettre en minuscule a,b,c,d,e,f ). | %bx | 8 bits |
| %X | Nombre hexadécimal (lettre en majuscule A,B,C,D,E,F). | %bX | 8 bits |
| %#X | Ajoute 0x devant le nombre hexadécimal. (petit bug si 0) |  |  |
| %s | Chaine de caractères. |  |  |
| %u | Nombre entier 16 bits non signé (positif seulement). | %bu | 8 bits |

Exemples:

|  |  |
| --- | --- |
| **Pseudocode** | **C** |
| ÉCRIRE "La moyenne est: ". ÉCRIRE Moyenne. | printf("La moyenne est: %f", Moyenne); |
| ÉCRIRE 'C'. | printf("%c", 'C'); ou printf("%c", 0x43); ou printf("C"); |
| ÉCRIRE Nom. // Nom: chaine. | printf("%s", Nom); |
| ÉCRIRE 12.26. | printf("%5.2f", 12.26); ou printf("12.26"); |
|  |  |

### 2.4.2. Exemples d'utilisation des formats avec printf( ):

|  |  |
| --- | --- |
| **Instructions** | **Affichage** |
| fValeur = 23.17; |  |
| printf("Valeur = %f", fValeur); | Valeur = 23.170000 |
| printf("Valeur = %4.2f ", fValeur); | Valeur = 23.17 |
| printf("Valeur = %5.2f ", fValeur); | Valeur = 23.17 |
| printf("Valeur = %7.2f ", fValeur); | Valeur = 23.17 |
| printf("Valeur = %07.2f ", fValeur); | Valeur = 0023.17 |
| iHeure = 8; iMin = 24; iSec = 7; |  |
| printf("Time = %d:%d:%d",iHeure,iMin,iSec); | Time = 8:24:7 |
| printf("Time = %2d:%2d:%2d",iHeure,iMin,iSec); | Time = 8:24: 7 |
| printf("Time = %02d:%02d:%02d",iHeure,iMin,iSec); | Time = 08:24:07 |
| printf("\nPort 3 = %02bu", ucReadPort(3)); | Port 3 = 207 |
| printf("\nPort 3 = 0x%02bX", ucReadPort(3)); | Port 3 = 0xCF |

## 2.4 (Notes complémentaires)

## Le format de l'argument du printf est:

"une chaîne de caractères" (entre guillemets)

Incluant :

* Les caractères à afficher tel quels
* Les codes de format ( répérés pas % )
* Un code de conversion (tel que c , d f ) qui précise le type de l'information à afficher - Des valeurs pour agir sur la précision
* Ex: %5.2f
* %05.2f

Suivie d'une virgule

Suivie du nom des variables séparés par des virgules

Ex: printf ("le nombre de morceaux comptés est de %d unités" , iNombre )

Si une variable se répète 2 fois dans la chaîne de caractères , il faut la nommer 2 fois après la virgule Ex: printf ("………%d.........%d……." , iVar1 , iVar1 )

Ex: printf ("…%d…" , iVar1 , iVar2 ) =NON printf ("…%d…..%d…." , iVar1 ) =NON

printf ("…%d…..%d…." , iVar1 , iVar2 ) = OUI

Types de variables

* int nombre entier
* float nombre à point flottant
* char caractère du clavier

Convention taxonomique des variables

Déclaration: type nom

Nom : - préfixe de type en minuscule , Nom

* Alphanumérique ( pas numérique seulement )
* L'initiale doit être une lettre ( on la met en majuscule )
* Attention: C distingue les minuscules des majuscules - Pas de mots réservés. Ex if , else , while

Déclaration des variables:

On doit déclarer les variables en début de programme

int main (void)

{

/\* USER CODE BEGIN 1 \*/

int iRayon = 1;

float fCirconf;

/\* USER CODE END 1 \*/

………………..

/\* USER CODE BEGIN WHILE \*/

Entrer le code à exécuter **avant** la boucle sans fin .

while (1)

Entrer le code à exécuter **dans** la boucle sans fin .

/\* USER CODE END WHILE \*/

* Quand on déclare une variable , on peut lui donner une valeur ( initialiser ) - int iRayon ;
* int iRayon = 2 ;
* Mais pas de getchar () dans la déclaration .

Résumé format dans un printf

int ------- %d , %x , %#x char ------- %c

Caractère de fin de string

En C les instructions se terminent par " ; "

* Retour à la ligne ou pas
* Ex: sur plusieurs lignes = OK

## 2.5. Lecture et écriture sur les ports:

**Algo**  **C**

LIRE ConvTemp au Port1. ucConvTemp = ucReadPort( 1 ); // 8 bits.

LIRE BoutonStart à P1\_4. ucBoutonStart = bReadPin( 1 , 4 ) ;

// 1 bit.

ECRIRE 0xFE au Port2. vWritePort( 0xFE , 2 );

ECRIRE Convertisseur au Port1. vWritePort( ucConvertisseur , 1 );

ECRIRE 0 à P1\_4. vWritePin( 1 , 4 , 0 );

ECRIRE EtatLed a P3\_5. vWritePin( 3 , 5 , ucEtatLed );

À noter que les fonctions ucReadPort et bReadPin placent les pins à ‘1’ . Ainsi , si un LED est branché sur un bit du Port , il va s’éteindre et nous ne pourrons pas lire son état .

## 2.6. Commentaires en langage C:

En langage C on utilise deux sortes de commentaires.

Le **premier** est le **commentaire de ligne** et il est identifié par les doubles barres obliques **//**. Tout le texte qui suit les barres obliques, n'est pas considéré par le compilateur. Le commentaire se termine avec la fin de la ligne.

Nos commentaires vont toujours **commencer par une majuscule** et se **terminer par un point**.

Exemples: // Commentaire en bout de ligne.

// Si le commentaire est vraiment trop // long, on peut le placer sur deux lignes.

Le **deuxième** type de commentaire sera utilisé **pour soustraire une partie de notre programme** à la compilation. Ce sera utile pour isoler les problèmes. Ce type de commentaire commence par la barre oblique suivit de l'étoile. Il se termine lorsque le compilateur trouve une étoile suivit de la barre oblique.

Exemple:

if ((fThermo < 25.0) || (fThermo > 35.0)) // Erreur?

{ cCloche = 0; // Active Cloche.

printf("\nCorrigez la temperature.\n");

}

**/\*** else // OK (25 <= Temp <= 35).

{ cCloche = 1; // Desactive Cloche.

} **\*/**

Le bloc "else" ne sera pas compilé car il est entre les marques de commentaires: /\*.....\*/.

## 2.7. Exemple d'utilisation des commentaires de ligne:

Exemple tiré d'un projet étudiant qui contrôlait un simulateur de maison. Si on pesait sur le bouton de la lumière pendant 2 secondes, on tombait dans le mode d'affichage de l'heure sur les 7 segments qui affiche normalement la température. L'heure était affichée durant 3 secondes, les minutes durant 3 secondes, ensuite on réaffiche la température et le bouton lumière redevient fonctionnel.

if(ucModeAff == HEURE) // Mode affichage de l'heure?

{

if (ucTempsInitL) < TAFFHEURE) // Pendant les 3 premieres secondes

{ // on affiche l'heure. uc7Seg = ucHeure;

}

else // Entre 3 et 6 secondes, on affiche

{ // les minutes. if (ucTempsInitL) < TAFFMINUTE)

{

uc7Seg = ucMinute;

}

else // Apres 6 secondes, on affiche la { // temperature actuelle a nouveau.

ucT = ucTempPiece;

// Formule de conversion HEX2BCD. uc7Seg = ucT + (((ucT - (ucT % 10)) / 10) \* 6); ucOldLum = INACTIF; // On permet a nouveau d'utiliser

// le bouton lumiere. ucModeAff = TEMPERATURE; // Retour au mode Temperature.

} //FIN du if(ucTempsInitL) < TAFFMINUTE)

} //FIN du if(ucTempsInitL) < TAFFHEURE)

} //FIN du if(ucModeAff == HEURE)

Notez l'**absence d'accent**: Certains compilateurs sont sensibles aux lettres accentuées. Les problèmes peuvent être simplement un affichage de drôles de caractères ou pire une erreur de lecture du compilateur, alors vos programmes ne seront pas compilés.

**À Noter :** Pour impression sur une imprimante , les lignes ne doivent pas dépasser 80 colonnes. Il y a une trait-repère dans l’éditeur IAR pour indiquer la marge droite des lignes

## 2.8. Entêtes:

Les commentaires seront aussi utilisés pour expliquer le fonctionnement d'un programme ou d'une partie de programme. Pour la première session ce sera la description de vos programmes qui sera inclus dans l'entête.

Voici un exemple d'information minimum à fournir pour un **entête de programme**:

/////////////////////////////////////////////////////////////////////////////// //

// Fichier: LAB9.C

//

// Description: - Programme du laboratoire #9 du cours 247-215.

// - Ce programme permet de lire et d'afficher, a l'ecran du PC,

// l'etat du simulateur de maison.

// - On peut aussi controler certains elements tel: // - L'etat des lumieres.

// - La temperature de consigne de chaque piece.

// - On peut modifier l'heure, les minutes et les secondes.

//

// Programmeur: Daniel Cote

//

// Date: 19/11/00

//

// Compilateur: Borland C 3.1

//

// Modification:

// 17/05/01: Corrige l'erreur pour la modification des minutes.

// 19/05/01: Enleve la boucle qui bloquait le programme lorsque

// le simulateur n'etait pas branche. Remplacer par un

// simple test.

///////////////////////////////////////////////////////////////////////////////

Parfois l'entête occupe plus de place que la section de programme qu'elle décrit. Ceci permet aux personnes consultant le programme de comprendre le fonctionnement du programme, sans nécessairement connaitre le langage de programmation.

Voici un exemple tiré du même programme de contrôle du simulateur de maison. C'est l'entête de la section qui s'occupe de l'affichage sur les 7 segments de chaque pièce.

Exemple d'entête de fonction:

////////////////////////// GereModeAffichage /////////////////////////////////

// Niveau : 2 Date de creation : 23-02-00

// Date de modification : 23-03-00

// Concepteur(s) : Gerard Brunelle

//

// Description : -On met a jour uc7Seg en fonction de ucModeAff.

// si HEURE, on affiche l'heure, suivit des secondes et // la temperature actuelle apres 6 secondes. // si TEMPERATURE, on affiche la temperature le la piece.

// si TCONSIGNE,

// si moins de 3 secondes, on affiche la temperature

// de consigne. // sinon, on affiche la temperature actuelle.

//

// Prototype : void GereModeAffichage(UC);

//

// Appelee par : -TraitementDemandes()

//

// Fonction(s) appelee(s) : -Aucune

//

// Variable(s) globale(s) : -uc7Seg: Information a afficher.

// -stRTC: Structure de donnees du RTC contenant,

// **ucHeure**, **ucMinute**.

// -Pi[]: Tableau de structures contenant les

// elements de controle :

// stLecture: Contient la structure de // lecture de chaque piece.

// stFuture: Contient la structure de // l'etat Future de chaque piece.

// **ucOldLum**: Aide au routage des fonctions // de gestion de la lumiere pour

// detecter les fronts.

// **ucTempsInitL**: Garde le temps ou on commence

// a appuyer sur le bouton.

// **ucModeAff**: Garde l'endroit ou chaque piece

// est rendue dans son affichage.

//

// Parametre(s) d'entree : -i, indice indiquant la piece traitee dans le

// tableau.

//

// Parametre(s) de sortie : -Aucun

//

// Version : Par : Modification(s) : // 24-02-00 Gerard Brunelle -Mise en forme.

// 13-03-00 Gerard Brunelle -Instauration du tableau de structures // Pi[] contenant les elements de controle.

// 23-03-00 Gerard Brunelle -On change les variables ucTempPiece et

// ucTempConsigne qui sont en format HEX

// pour le format BCD afin de le envoyer

// dans uc7Seg de stFuture. //

// Compilateur : IAR Embedded Workbench 2.21C

//////////////////////////////////////////////////////////////////////////////

## 2.9. Les opérateurs logiques:

En langage C nous aurons besoin d'opérateur pour nous permettre d'effectuer nos tests avec des ET et des OU.

Équivalence:

|  |  |
| --- | --- |
| **Algo** | **C** |
| **ET** | **&&** // Le ET logique. Permet |
|  | // de joindre deux tests. |
| SI((Touche == 0x0A) ET (Temp > 28)) | if((iTouche == 0x0A) && (iTemp > 28)) |
| **OU** | **||** // Le OU logique. Permet de |
|  | // choisir un test ou l'autre. |
| SI((Key == 'Q') OU (Key == 'q')) | if((iKey == 'Q') || (iKey == 'q')) |

Exemples: Trouvez le test pour partir un moteur si la température est supérieure à 40 degrés ou si un bouton est pesé.

SI((Temp > 40) OU (Bouton == 1)) if((fTemp > 40) || (iBouton == 1))

Trouvez le test pour vérifier si le niveau maximum est atteint et si le moteur de la pompe est en marche.

SI((Niveau > MAX) ET (Pompe == ON)) if((fNiveau > MAX) && (iPompe == ON))

## 2.10. Code ASCII, Hexa décimal, Binaire, Décimal:

**Nombre binaire:**

La plus petite unité d'information dans un ordinateur se nomme le "BIT". Elle peut prendre deux valeurs, 0 ou 1.

Le BIT n'est pas très pratique si on le prend tout seul (seulement 2 valeurs). On a donc choisit de prendre des groupes de bits. On va appeler ces groupes des MOTS. Le nombre de bits dans le mot détermine sa longueur. Exemple un mot de 8 bits, un mot de 12 bits etc…

Nom de mots spéciaux: 8 bits Octet (byte) Le plus connu des mots.

16 bits Mot 16 bits (word)

4 bits quartet (nibble)

Bases de numération (binaire, hexadécimal, décimal):

- Un nombre binaire est représenté par l'état 0 ou 1 de plusieurs bits.

Exemple: 101100

## 2.11. Valeur décimal d'un nombre binaire (Bin Déc):

Un nombre binaire est formé d'un polynome: (…. a4\*24 + a3\*23 + a2\*22 + a1\*21 + a0\*20)

Les coefficients "ax" peuvent prendre la valeur 0 ou 1.

Exemple précédent:

101100 = 1\*25 + 0\*24 + 1\*23 + 1\*22 + 0\*21 + 0\*20

= 32 + 0 + 8 + 4 + 0 + 0 = 44 décimal.

Autre technique: (+ rapide)

1024 512 256 128 64 32 16 8 4 2 1  Multiples de 2

1 0 1 1 0 0  Mon nombre

32 8 4 = 44  Résultat

Exercices: Transformez en décimal les nombres binaires suivants:

0101 1101: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

1100 1001: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## 2.12. Valeur binaire d'un nombre décimal (Déc  Bin):

La méthode traditionnelle utilise la décomposition par division successive:

Exemple: 37 décimal = ? binaire

|  |  |  |
| --- | --- | --- |
|  | |  | | --- | | Méthode personnel avec multiple de 2:  128 64 32 16 8 4 2 1 37: 1 0 0 1 0 1 reste reste  5 1 | |

37 / 2 = 18 reste 1

18 / 2 = 9 reste 0

9 / 2 = 4 reste 1

4 / 2 = 2 reste 0

2 / 2 = 1 reste 0

1 / 2 = 0 reste 1

Résultat: 1 0 0 1 0 1

Exercices: Transformez en binaire les nombres décimaux suivants:

149: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

231: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## 2.13. Hexadécimal.

Représentation d'un nombre binaire pris quatre bits à la fois (quartet).

Avec 4 bits on peut avoir 16 possibilités: 4 bits  24  16 nombres différents (0 à 9 et A à F).

|  |  |  |
| --- | --- | --- |
| 4 BITS | Hexadécimal | Décimal |
| 8 4 2 1 |  Poid des bits | |
| 0 0 0 0 | 0 | 0 |
| 0 0 0 1 | 1 | 1 |
| 0 0 1 0 | 2 | 2 |
| 0 0 1 1 | 3 | 3 |
| 0 1 0 0 | 4 | 4 |
| 0 1 0 1 | 5 | 5 |
| 0 1 1 0 | 6 | 6 |
| 0 1 1 1 | 7 | 7 |
| 1 0 0 0 | 8 | 8 |
| 1 0 0 1 | 9 | 9 |
| 1 0 1 0 | A | 10 |
| 1 0 1 1 | B | 11 |
| 1 1 0 0 | C | 12 |
| 1 1 0 1 | D | 13 |
| 1 1 1 0 | E | 14 |
| 1 1 1 1 | F | 15 |
| Suivant? |  |  |

**Bin**  **Hexa:** On prend les bits en paquet de 4 à partir de la **droite.**

Exemple (1101110110):

1 1 / 0 1 1 1 / 0 1 1 0

3 7 6 Donc: 0x376

Exemple (101101011100):

1 0 1 1 / 0 1 0 1 / 1 1 0 0

B 5 C Donc: 0xB5C

**Hexa**  **Bin:** Chaque digit représente 4 bits.

Exemple (0x198):

0x 1 9 8

0001 1001 1000 Binaire

Exemple (0x7EB6):

0x 7 E B 6

0111 1110 1011 0110 Binaire

Faire l'exercice.

Théorie sur les opérateurs binaires (de bits)

Nous verrons les opérateurs suivants: & ET

| OU

^ OU-Exclusif

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Entrées | |  | Opérateurs |  |
| A | B | **&** (ET) | **|** (OU) | **^** (OU Ex) |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 |

|  |  |  |
| --- | --- | --- |
| A |      Opérateur | Sortie |
| B |
|  |
|  |

Table de vérité:



* Les opérateurs binaires sont utilisés pour modifier un ou plusieurs bits à la fois.

* On les utilisera aussi pour isoler un groupe de bit.

* Ces opérateurs sont utilisés entre deux opérandes (données).

* Un des opérandes est souvent appelé un masque.

* L'exécution de l'opérateur s'effectue entre chaque bit des deux opérandes.

* L'opérateur ET ( & ) est souvent utilisé pour **mettre des bits à 0** ou pour **isoler un groupe de bits**.

* L'opérateur OU ( | ) est souvent utilisé pour **mettre des bits à 1**.

* L'opérateur OU-Exclusif ( ^ ) est souvent utilisé pour **changer l'état des bits**.

### 2.13.1. Exemples avec données à 8 bits:

**ET:**

0xFF  1111 1111 (Donnée)

& &

0xFE  1111 111**0** (Masque, **le ET met les bits à 0**)

-------------------

Résultat: 1111 111**0**

En C: cResultat = 0xFF & 0xFE; // Apres execution, cResultat contient 0xFE.

Exercices:

cResultat = 0x0F & 0xF0; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

cResultat = 0xAB & 0x27; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

cResultat = 0xAA & 0x55; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**OU:**

0x00  0000 0000 (Donnée)

| |

0x01  0000 000**1** (Masque, **le OU met les bits à 1**)

-------------------

Résultat: 0000 000**1**

En C: cResultat = 0x00 | 0x01; // Apres execution, cResultat contient 0x01.

Exercices:

cResultat = 0x0F | 0xF0; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

cResultat = 0xAB | 0x27; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

cResultat = 0x10 | 0x01; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

cResultat = 0xAA | 0x55; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**OU Exclusif:**

0xF0  111**1** 000**0** (Donnée)

^ ^

0x11  000**1** 000**1** (Masque, **le OU EX change l'état des bits**)

------------------- (à l'endroit où le masque a des 1.)

Résultat: 111**0** 000**1**

En C: cResultat = 0xF0 ^ 0x11; // Apres execution, cResultat contient 0xE1.

Exercices:

cResultat = 0x0F ^ 0xF0; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

cResultat = 0xAB ^ 0x27; // cResultat = \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

### 2.13.2. Exemples avec données à 16 bits:

**ET:** F 0 A C

0xF0AC  1111 0000 1010 1100 (Donnée)

& &

0x93F6  1**00**1 **00**11 1111 **0**11**0** (Masque, le ET met les bits à 0)

-------------------

Résultat: 1**00**1 **00**00 1010 **0**10**0**

En C: iResultat = 0xF0AC & 0x93F6; // iResultat = 0x90A4

**OU:** 8 7 9 2

0x8792  1000 0111 1001 0010 (Donnée)

| |

0x7349  0**111** 00**11** 0**1**00 **1**00**1** (Masque, le OU met les bits à 1)

-------------------

Résultat: 1**111** 01**11** 1**1**01 **1**01**1**

En C: iResultat = 0x8792 | 0x7349; // iResultat = 0xF7DB

**OU Exclusif:** B 4 C E

0xB4CE  1011 010**0** **1100** 1110 (Donnée)

^ ^

0x01F9  0000 000**1** **1111** **1**00**1** (Masque, le OU EX change l'état des bits)

------------------- (à l'endroit où le masque a des 1.)

Résultat: 1011 010**1** **0011** **0**11**1**

En C: iRésultat = 0xB4CE ^ 0x01F9; // iResultat = 0xB537

**ET (pour isoler un groupe de bits):**

0xF2AC  1111 0010 1010 1100 (Donnée)

& &

0x03F0  **0000 00**11 1111 **0000** (Masque, le ET met les bits non désirés, à 0)

-------------------

Résultat: **0000 00**10 1010 **0000**

En C: iRésultat = 0xF2AC & 0x03F0; // iResultat = 0x02A0

### 2.13.3. Exemples en C (isoler des bits pour les tester):

|  |  |
| --- | --- |
| if( (ucReadPort(2) & 0x04) == 0x04) | // Vérifie si l'entrée P2.2 est à 1. |
| if( (ucReadPort(2) & 0x04) == 0x00) | // Vérifie si l'entrée P3.2 est à 0. |
| if( (ucReadPort(1) & 0x38) == 0x38) | // Vérifie si les bits 3,4 et 5 du |
|  | // Port1 sont à 1. |
| if( (ucReadPort(1) & 0x38) != 0x38) | // Vérifie si un des bits 3,4 ou 5 |
| Hexa | // du Port1 est à 0. |
| if( (ucReadPort(1) & 0x38) == 0x00) | // Vérifie si les bits 3,4 et 5 |
|  | // du Port1 sont à 0. |

printf("Etat du bit P2.0: 0x%bX", (ucReadPort(2) & 0x01); // Valeurs

// possibles: 0x0 ou 0x1

## 2.14. Branchement d'interrupteur ou de bouton poussoir sur le port d'un microcontrôleur:

Normalement nous utiliserons des résistances de Pull-Up VCC pour amener le niveau logique '1' sur la broche du port.

uProc

P1.6

P1.5

P1.4

SW1

SW2

SW3

R1

4

7

k

R2

4

7

k

R3

7

4

k

La valeur de la résistance devrait être entre 2.2 kΩ et 10 kΩ.

Idéalement, la valeur de la résistance devrait être la plus élevée possible pour limiter le courant. Cependant, une valeur trop grande peut diminuer le temps de réaction du système ou encore empêcher d'avoir un bon niveau '1'. Par exemple 100 kΩ serait une valeur un peu élevée.

Le niveau '0' sera amené sur la broche du port par l'entremise de l'interrupteur. Si le bouton est pesé on va lire un niveau '0' (GND)

Attention: Pour que ce circuit fonctionne, il faut que les bits du port soient en **entrées**. La plupart des microprocesseurs placent leurs ports en entrées au démarrage. Pour placer un bit de port en entrée il s'agit souvent de mettre tout simplement **un '1' sur le bit du port**.

Quelquefois, il faut écrire dans un registre de direction du microprocesseur pour indiquer que le bit est en entrée.

Pour la résistance de Pull-Up, certains microprocesseurs en ont une interne. Parfois, elle est toujours active et pour d'autres processeurs, il faut l'activer. Dans le cas du STM32 , il faut l’activer .

Si on a plusieurs Pull-Up à placer sur un port, il peut être intéressant d'utiliser des résistances montées en ligne (SIP Single Inline Package).

R4

RESISTOR SIP 8

1

2

3

4

5

6

7

8

VCC

**Lire un port**: La lecture du port se fait en utilisant la fonction ucReadPort() dans une expression (souvent à droite du =).

|  |  |
| --- | --- |
| ucPort2 = ucReadPort(2); | // Lecture du port P2. |
| printf("ucPort2 = %02bX", ucReadPort(2)); | // Affiche P2 en hexa. |
| ucBit0Port2 = ucReadPort(2) & 0x01; | // ucBit0Port2 vaut 0 ou 1. |
| ucBit3Port2 = ucReadPort(2) & 0x08; | // ucBit3Port2 vaut 0 ou 8. |
| ucBit6Port2 = ucReadPort(2) & 0x40; | // ucBit6Port2 vaut 0 ou 0x40. |

## 2.15. Isoler des bits en lecture pour traiter l'information lue

**sur plusieurs bits.** VCC

Par exemple on veut lire les trois interrupteurs de la page précédente (P1.4 à P1.6).

uProc

P1.6

P1.5

P1.4

SW1

SW2

SW3

R1

2

2

k

R2

2

k

2

R3

2

2

k

Il s'agit ici de modifier le masque pour englober les trois bits.

Bit# 76543210

Masque = 01110000 (0x70)

Sw = ucReadPort(1) & 0x70; // Lecture Switch sur P1.

Vérifier si **un** interrupteur a été **pesé**, il sera alors à 0 (exemple P1.4)

if((Sw & 0x10) == 0) // SW1 Pese? (P1.4 == 0)

Vérifier si **un** interrupteur n'est **pas pesé**, il sera alors à 1 (exemple P1.5)

if((Sw & 0x20) == 0x20) // SW2 Pas Pese?(P1.5 == 1)

if(Sw & 0x20) // Pourquoi ça marche?

Vérifier si **un des** interrupteurs a été **pesé**, il y aura alors au moins un 0 dans les trois.

if((Sw & 0x70) != 0x70) // Un interrupteur pesé?.

Vérifier si **tous** les interrupteurs sont **pesés**, il y aura alors trois 0

if((Sw & 0x70) == 0) // Tous pesés?

{

// Instructions si tous pesés.

}

else // Pas tous pesés.

{

// Instructions si pas tous pesés.

}

**Écriture sur les ports**. L'écriture sur un port se fait avec la fonction vWritePort( donnée , Port )

Exemples (avec le port 2):

|  |  |
| --- | --- |
| vWritePort(0xEF,2); | // Met P2.4 a 0 **et** les **autres bits a 1**. |
| vWritePort(ucP2 & 0xEF , 2); | // Met P2.4 a 0, **les autres sont inchangés.** |
| vWritePort(ucP2 | 0x10 , 2); | // Met P2.4 a 1, **les autres sont inchangés.** |
| vWritePort(ucP2 ^ 0x10 , 2); | // Change état P2.4, **les autres sont inchangés.** |
| vWritePort(ucVariable , 2); | // Active les éléments du port 2. |

**En général nous utiliserons une variable pour mémoriser l'état du port, surtout si le port est modifié à plusieurs endroits dans le programme**.

## 2.16. Branchement interne d'un bit de port (1 et 2) du STM32F103

Schéma simplifié d'une broche d’un Port :

Pin 1.xI?

2V

LED

Si on écrit un '1' sur le bit de port:

La tension en sortie vient du transistor T1.

Le microcontrôleur ne sera pas capable de fournir suffisamment de courant. Nous ne pouvons pas activer, avec un '1', des éléments qui demandent beaucoup de courant.

Nous allons donc écrire un '0' sur le bit de port:

Le Port sera configuré en entrée open-collector (nous verrons ceci dans un autre cours).

La tension en sortie sera ici fournie par le transistor T2.

Pour le STM32F103, avec un '0' en sortie nous allons limiter le courant à **8ma**.

La documentation de STM nous demande de ne pas dépasser 25ma pour les 8 bits d'un port (ce que nous ferons mais ce n'est pas garantie).

|  |  |
| --- | --- |
|  | |
|  | P2.5 P2.4 |
|  |

 R5470

LED



VCC



## 2.17. Structure des programmes avec Délai

Structure des programmes utilisant une boucle de délai pour ralentir le programme afin de nous permettre de visualiser des phénomènes externes (exemple: Led qui clignote).

La boucle externe dure une milliseconde.

Le nombre de ms sera dans la variable uiDelai et la valeur maximum sera de 65535.

void main(void)

{ unsigned int uiDelai = 0; // Si non modifiee dans le pgm, aucun delai.

unsigned int uiDelaiIn; unsigned int uiDelaiOut;

while(1)

{

// Lecture des entrees. // On met la valeur des ports dans des variables.

// Exemple: ucPort1 = ucReadPort( 1 );

// Traitement // Exemple: ucPort1 = ucPort1 & 0x7F. //Bit7 a 0.

- - uiDelai = 1000; // Dans le pgm on veut un delai de 1 seconde.

-

-

// Ecriture des resultats. // On met la valeur des variables dans les ports.

// Exemple: vWritePort( ucPort1 , 1 );

// Delai uiDelaiOut = 0; while (uiDelaiOut < uiDelai) // Boucle de uiDelai millisecondes.

{

uiDelaiOut++; uiDelaiIn = 0; while(uiDelaiIn < 8500) // 8500: Valeur trouvée de maniere experimentale { // pour avoir 1 milliseconde par boucle uiDelaiIn++; // avec un STM32F103xx a 8 MHz.

}

}

} // Fin while(1).

} // Fin main.

## 2.18. Types de Données

À ce jour, nous avons toujours utilisé les types "int" et "float". Pour nos besoins, ces types de données suffisaient. Le langage C, est un langage près du matériel (électronique). Il est optimisé pour une utilisation efficace du code. C'est pourquoi il est très utilisé dans des environnements où les ressources matérielles sont limitées. Par exemple, dans plusieurs microcontrôleurs l'espace mémoire est relativement faible (128 octets de RAM par exemple). Il est donc important d'utiliser le bon type de donnée en fonction des besoins, afin de ne pas gaspiller des bits qui sont si précieux.

Par exemple, si nous utilisons toujours des variables entières pour mémoriser l'état d'un bit (0 ou 1), on perd beaucoup d'espace à chaque fois, car un entier (int) est à 16 bits. Il existe en C, des types de donnée moins gourmands en espace mémoire.

Plusieurs types de donnée sont standard en C et d'autres sont spécifiques au compilateur utilisé.

Voici quelques types standards en C.

|  |  |  |  |
| --- | --- | --- | --- |
| Types | Nombre de bits | Nombre d'octets | Plage |
| char | 8 | 1 | -128 à +127 |
| int\* | 16 | 2 | -32768 à +32767 |
| float | 32 | 4 | ±3.4\*10-38 à ±3.4\*10+38 + 0 |
| long | 32 | 4 | -2 147 483 648 à +2 147 483 647 |
|  |  |  |  |

\* Le type "int" peut être à 32 bits dans certains environnements. Pour être sûr d'avoir une variable à 16 bits, il existe le type "short".

Regardons le type "char". C'est un type à 8 bits donc 28 = 256 possibilités (-128 à +127)

Pourquoi +127 et non pas +128?

+127 en binaire  0111 1111

Le huitième bit est à zéro. Si ce bit devient 1, nous aurons un nombre négatif. On dit alors que le bit le plus significatif est le bit de signe. Les nombres négatifs sont codés en complément à deux. Nous verrons ce codage dans un cours ultérieur. Sachez pour l'instant que 0000 0000 – 0000 0001 = 1111 1111 = -1.

S'il existe des types de variables avec un signe, il existe aussi des types non signés (toujours positif). Voici les principaux:

|  |  |  |  |
| --- | --- | --- | --- |
| Types | Nombre de bits | Nombre d'octets | Plage |
| unsigned char | 8 | 1 | 0 à +255 |
| unsigned int | 16 | 2 | 0 à +65535 |
| unsigned long | 32 | 4 | 0 à +4 294 967 295 |
|  |  |  |  |

Le type à 8 bits est particulièrement intéressant pour nous. Plusieurs registres du processeur sont à 8 bits (exemple les ports). Donc le type "unsigned char" sera très utilisé dans nos programmes.

Le type "unsigned int" sera souvent utilisé comme indice de boucle ou pour faire des calculs d'entier avec de petites valeurs positives.

Finalement, le type "float" sera utilisé exclusivement pour des calculs nécessitant la partie décimale. Ce genre de donnée demande beaucoup de ressource du processeur. Les calculs utilisant les points flottants demandent beaucoup de temps et d'espace mémoire. Dans la mesure du possible évité l'emploi du type "float" pour de petits processeurs.

Nous voici donc avec une panoplie de type différent.

À partir de maintenant, **nous devrons identifier le type de la variable** dans le nom de la variable. Il sera alors, plus facile de vérifier nos programmes. La manière de procéder est simple. Il s'agit de mettre un **préfixe à nos variables.** Ce préfixe identifiera le type de donnée.

Liste des préfixes:

|  |  |  |
| --- | --- | --- |
| Types | Préfixe | Exemple (nom de variable) |
| char | c | cPetitCalcul |
| unsigned char | uc | ucPort1 |
| int | i | iCalculMoyen |
| unsigned int | ui | uiBoucle |
| long | l | lGrandCalcul |
| unsigned long | ul | ulGrandNombrePositif |
| float | f | fCalculPointFlottant |
|  |  |  |

Rappel pour le nom de nos variables:

1. Commence par un préfixe qui identifie le type de la variable.
2. Chaque mot important dans le nom de la variable, commence par une majuscule.

**Cas particulier** (Microcontrôleurs basés sur des bits (bit-oriented))

-SFR :

Certains compilateurs ont été optimisés pour tenir compte de l'architecture interne des microcontrôleurs de la famille 8051. Ces processeurs ont des registres spéciaux nommés les SFR (Special Fonction Registers). Ces registres sont placés dans le processeur à des adresses spécifiques. Pour y accéder, il faudra utiliser le type "sfr". C'est un type non standard en C.

-SBIT :

Un autre type que vous pourrez rencontrer est "sbit". Avec ce type on peut accéder à un seul bit à la fois, dans certaines zones du processeur. Les ports font partie de cette zone. Donc, si on place des déclarations au début de notre programme (ça peut être dans un fichier .h) nous pourrons accéder individuellement à chaque bit du port 1

-BOOL :

En C, le type de données bool n'est pas un type de données intégré. Cependant, la norme C99 pour le langage C prend en charge les variables booléennes. Bool peut stocker des valeurs comme vrai-faux, 0-1 ou oui-non.

En fait, en C, le type booléen n’est pas implanté en tant que tel : un booléen est représenté par un entier : si b est une variable de type entier, b correspondra à la valeur faux si b vaut l’entier 0 et à vrai si b vaut l’entier 1.

Traditionnellement, on prend 1 comme valeur pour vrai. Cela dit, il vaut mieux utiliser le type bool et les constantes true et false pour des raisons de lisibilité.

Un type de données booléen est déclaré avec le mot-clé bool et ne peut prendre que les valeurs vraies ou fausses.

Lorsque la valeur est renvoyée, true = 1 et false = 0.

La meilleure façon de définir un booléen est d'utiliser la définition introduite par la norme du langage C99.

#include <stdbool.h>

bool bVariable ;

Dans le câdre de ce cours , nous allons plutôt l’utiliser pour ne traiter qu’un seul bit avec les fonctions bReadPin(Port , Pin) et vWritePin(Port , Pin , Etat).

Pour terminer, voici quelques types disponibles avec STM32.

## Integer Data Types

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **C type** | **stdint.h type** | **Bits** | **Sign** | **Range** |
| char | uint8\_t | 8 | Unsigned | 0 .. 255 |
| signed char | int8\_t | 8 | Signed | -128 .. 127 |
| unsigned short | uint16\_t | 16 16 32 32 | Unsigned | 0 .. 65,535 |
| short | int16\_t | Signed | -32,768 .. 32,767 |
| unsigned int | uint32\_t | Unsigned | 0 .. 4,294,967,295 |
| int | int32\_t | Signed | -2,147,483,648 .. 2,147,483,647 |
| unsigned long long | uint64\_t | 64 | Unsigned | 0 .. 18,446,744,073,709,551,615 |
| long long | int64\_t | 64 | Signed | -9,223,372,036,854,775,808 ..  9,223,372,036,854,775,807 |

## Floating Point Data Types

|  |  |  |  |
| --- | --- | --- | --- |
| **C type** | **IEE754 Name** | **Bits**  32  64 | **Range** |
| float | Single Precision  Double Precision | -3.4E38 .. 3.4E38 |
| double | -1.7E308 .. 1.7E308 |

## 2.19. Les Constantes:

Comme nous l'avons déjà vu, il y a plusieurs types de donnée en C (char, int, float, unsigned char, etc.). Pour chacun de ces types correspond un ensemble de valeur fixe que l'on appelle constantes.

Constantes entières:

On peut les définir dans plusieurs formats correspondant à différentes bases de codage de nombre.

**Base décimal:** C'est la base 10 ( 0 à 9), le format usuel des entiers.

Exemple.: 35, 339, 123, etc.

**Base hexadécimal:** C'est la base 16 (0 à 9, a,b,c,d,e,f (minuscule ou majuscule)), format qui nous sera utile lorsque l'on voudra représenter des éléments plus près de la machine. On peut distinguer un nombre hexadécimal d'un nombre décimal par le fait qu'il est précédé par 0X ou 0x.

Exemple.: 0x3FA , 0X3333, 0x12

Note: On retrouve également la base octale mais elle est de moins en moins utilisée. Vous pourrez consulter un ouvrage de référence pour obtenir plus d'information.

Constantes flottantes:

On peut représenter les nombres flottants de deux (2) façons :

Notation littérale:

Exemple.: 12.3456

Notation scientifique :

Exemple.: 1.23456 e1

Constantes caractères:

On peut représenter les constantes caractères de deux (2) façons:

Valeur du caractère entre apostrophes.

Exemple : 'a' , 'B'

Valeur du code ASCII en hexadécimal précédé de la barre oblique et entre apostrophe.

Exemple.: '\0x61', '\0x42' (représente les caractères a et B)

Il existe aussi, un ensemble de caractères spéciaux que l'on nomme caractères de contrôle qui évite d'avoir à indiquer la valeur numérique du code ASCII.

|  |  |  |  |
| --- | --- | --- | --- |
| CODE | VALEUR | CARACTÈRE | UTILISATION |
| '\a' | 0x07 | BEL | Signal sonore |
| '\b' | 0x08 | BS | Retour en arrière (Back Space) |
| '\n' | 0x0A | LF | Saut de ligne (Line Feed) |
| '\r' | 0x0D | CR | Retour au début de la ligne (Carriage Return) |
| '\\' | 0x5c | \ | Barre oblique |
| '\'' | 0x27 | ' | Apostrophe |
| '\"' | 0x22 | " | Guillemet |

Finalement, l'utilisation répétitive de constante dans un programme en C, rend la lecture du programme plus difficile. C'est une bonne technique de programmation que d'utiliser un nom pour représenter une constante.

Exemple: ucMode = MANUEL; // Place le simulateur en mode Manuel.

En C, il est possible d'associer un nom à une constante avec la commande au préprocesseur: **#define**

Exemple:

#define DELAI 32000 // Notez: pas de ';' à la fin de la ligne.

void main(void)

{

int iBoucle = 0;

while(iBoucle < DELAI)

{

iBoucle = iBoucle + 1;

}

}

Avec l'utilisation de la constante DELAI, il est possible de modifier le délai dans tout le programme en modifiant seulement la définition de la constante au début du programme.

* Les #define, se placent à la suite des #include dans la section /\* Private define \*/ - /\* USER CODE BEGIN PD \*/.
* Le nom utilisé, est toujours en MAJUSCULE.
* La constante peut être de type caractère ou numérique (entier ou float).

**Dans les faits** le compilateur, lorsqu'il rencontre une constante, remplace le nom en majuscule par la valeur qui a été définie au début du programme.

## 2.20. Détecter un changement sur un signal

Jusqu'à maintenant, nous ne nous sommes pas trop souciés de la vitesse d'exécution de nos programmes (hormis les délais pour les DEL). Lors de la lecture des boutons, nous testons si le bouton est pesé ou non. Cependant, il arrive fréquemment que nous ne voulons pas agir tant que le bouton est pesé, mais seulement au moment où le bouton est pesé.

Voici le niveau électrique à l'entrée du port 2, bit P2\_4, lorsque le bouton de votre kit est pesé.

Bouton pesé

Bouton pas pesé

Bouton pas pesé

5

Volts

0

Volt

Ce qui nous intéresse, lors de la détection des changements, ce sont les transitions (descente ou montée). Elles sont indiquées par des flèches sur le dessin. On va souvent parler de front.

Pour faire réagir notre programme seulement lors des transitions, il faut être en mesure de détecter ces fronts. Pour y arriver, il faut connaître l'état actuel du bouton et l'état du bouton avant la dernière lecture. Si les deux valeurs sont identiques, alors il n'y a pas eu de changement. Cependant, si les deux valeurs diffèrent, nous pourrons conclure à un changement.

Pour mémoriser l'ancienne valeur du bouton, nous aurons donc besoin d'une variable. Cette variable sera initialisée au début du programme avec la valeur du bouton au début.

Exemple avec un bouton servant à la remise à zéro d'un compteur (branché sur P2\_4):

bool bAncienEtat; // Declaration de la variable.

...

bAncienEtat = bReadPin(2 , 4); // Initialisation de la variable. ...

while(1)

Pour détecter un changement il nous reste à vérifier si bAncienEtat est différent de la valeur actuel du bouton.

Exemple:

bNouvelEtat = bReadPin(2,4); // Lecture du bouton Marche. if(bAncienEtat != bBoutonMarche) // Changement du bouton Marche?

{

bAncienEtat = bBoutonMarche; // Il y a eu un changement. La valeur // actuel du bouton devient l'ancien etat. // Mettre ici le code a executer lors de la détection d'un changement. }

Nous avons donc détecté un changement. Nous ne savons toutefois pas si c'est une transition montante (on a relâché le bouton) ou une transition descendante (on vient de peser sur le bouton).

La valeur de bNouvelEtat nous donne cette information. Si bNouvelEtat est à 1, alors c'était un front de montée (on a relâché le bouton) sinon (bNouvelEtat est à 0) on vient de peser sur le bouton. Pour vérifier le type de transition, il faut simplement ajouter le code suivant dans le if( ).

if(bAncienEtat != bNouvelEtat) // Changement du bouton Marche?

{ bAncienEtat = bNouvelEtat; // Sauvegarde le nouvel etat.

if(bNouvelEtat == 1) // Front de monte?

{

// Mettre ici le code a executer si le bouton a ete relache.

} else // Front de descente.

{

// Mettre ici le code a executer si le bouton a ete pese.

}

}

Cette technique fonctionne avec n'importe quel signal.

Malheureusement, cette technique ne règle pas tous les problèmes.

Lorsque l'on pèse sur un bouton, il se produit un phénomène mécanique qui se nomme le rebondissement. Il s'agit d'un mouvement oscillatoire des contacts de l'interrupteur. Il s'en suit une série de contact/non-contact de l'interrupteur.

Si on regarde au niveau électrique (phénomène amplifié):

5Volts

0Volt

Bouton pesé Bouton relâché

On remarque sur cette forme d'onde que plusieurs transitions se produisent lorsqu'on pèse ou relâche le bouton. Donc même avec la technique de détection des changements, nous allons voir plusieurs changements alors qu'il ne doit y en avoir qu'un seul.

Voir page suivante pour Bouton réel.

Il existe plusieurs moyens pour résoudre le problème. Les techniques peuvent être matériel (ajout d'une bascule, ajout d'un condensateur, utilisation de bouton de meilleure qualité, etc…) ou logiciel.

Pour résoudre le problème de manière logiciel, on a besoin de savoir que ces oscillations durent en général moins de **10ms**. Donc, au moment de la détection du front, on ajoute un délai de 10 ms avant de continuer le programme. Ensuite si le programme revient voir l'état du bouton, il sera stabilisé.

Certains pourrons observer le phénomène du rebondissement à la section 7 du laboratoire 8.

Rebondissement d’un interrupteur

50 ms/div 20ms/div



5 ms/div 0.5 ms/div



0.1 ms/div



5V

1 V/div

0V

## 2.21. Notion de multiplexage

Schéma de deux afficheurs 7-segments:

Donnée

2

1

Commande 1

Commande 2

Une seule source de donnée pour deux affichages??

Question: On procède comment?

Rép: On partage le temps pour l'affichage de l'information. Un 7-segments à la fois.

Question: À quelle vitesse procède-t-on?

Rép: À 60Hz on ne voit plus le clignotement des lumières. 60Hz = 1 / T où T est la période.

T = 1/60 = 0.0166 sec ou 16.6 ms

Procédure:

1. On désactive les deux commandes
2. On met la Donnée 1 sur le bus de Donnée
3. On active la commande 1
4. On attend 16.6ms / 2 Pourquoi / 2?
5. On désactive les deux commandes
6. On place la donnée 2 sur le bus de donnée
7. On active la commande 2
8. On attend 16.6ms / 2
9. On recommence à l'étape 1, assez souvent pour que l'œil mémorise l'information.

Donc la **fréquence de balayage** sera de 16.6 ms / 2

Il faudra aussi trouver la **durée nécessaire d'affichage** pour que l'œil puisse mémoriser l'information. Un peu plus difficile à trouver, mais si on se rappelle qu'à 16.6 ms l'œil n'y voit que du feu, il faudra être plus lent.

Avec au moins 200 ms entre deux informations différentes (on change la Donnée 1 et la Donnée 2) l'œil commence à percevoir les données.