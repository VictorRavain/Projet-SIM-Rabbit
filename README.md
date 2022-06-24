# Projet SIM-Rabbit et Lapin automate

## Projet visant à développer un automate simulant les fonctions vitales d'un lapin

Le projet Sim Rabbit vise à développer, pour les travaux pratiques de physiologie expérimentale, un automate qui simule le comportement d’un lapin vivant, en particulier les variations de sa pression artérielle, de sa diurèse*, ou encore de sa fréquence ventilatoire et cardiaque en réponse à l’injection de différentes substances ou à la stimulation nerveuse.

À terme, le but du projet est la construction d'un lapin automate, prêt à l’emploi pour les futurs travaux pratiques vétérinaires. Le lapin sera accompagné d’une interface logicielle sur laquelle les étudiants pourront injecter numériquement des doses de substance dans le lapin et observer les tracés de la réponse du lapin aux différentes injections. Le lapin automate devra avoir des réactions réalistes en fonction des injections.

Les fonctions vitales sont constituées du rythme cardiaque, de la fréquence respiratoire et d’un signal sonore répétitif représentatif de la diurèse. Ils seront glissés dans un lapin en silicone pour permettre un gonflement des poumons et les vibrations du cœur. L’électronique permettant le pilotage sera déplacée et cachée pour avoir un final plus réaliste.


## Fichiers de données
On considère deux types donnée: cardio-respiratoire et cardio-rénale.
Les tracés issus d'un séance de travaux pratiques sont classés par année puis par *nom* de la séance.
Par exemple: `Data_2016/BlancheNeige`.

Une séance de TP est découpée en plusieurs fichiers de texte, un par séquence.
Chaque fichier porte le nom de la séquence et est compressé au format lzma.
Le séparateur est la tabulation (`\t`).
Une séquence correspond à un état de l'animal et reporte l'évolution de différentes constantes au cours du temps.
Les constantes observées différent d'un type de TP à l'autre.
Par exemple, un fichier nommé `Sansinjection.txt.lzma` est un fichier compressé décrivant
différentes constantes alors que l'animal n'a encore subit aucune injection.
A l'inverse, `Adrenaline.txt.lzma` reporte l'évolution, avec le temps, des différentes constantes enregistrées suite à l'injection d'adrenalyne.


### Cardio réspiratoire
Les fichiers se trouvent dans `./public/gdata/Cardio_Respi/` et sont classés en sous-dossiers.

Par convention, les fichiers de ce dossier ont le format suivant:

```txt
Time        PA          SP  PA moy.     FC          FR
1350,05     1280,039    0   1169,866    154,7285    20,66807
1350,051    1280,039    0   1169,866    154,7285    20,66807
1350,052    1280,039    0   1169,866    154,7285    20,66807
...
```
L'en-tête doit être présente mais est ignoré lors du chargement du fichier.
Les colonnes sont les suivantes:
- `Time` : horodatage de la ligne (il y a une ligne toutes les 5ms).
- `PA` : Pression Artérielle
- `SP` : Spirometrie
- `PA moy.` : PA moyenne
- `FC` : Fréquence Cardiaque 
- `FR` : Fréquence Respiratoire

L'ordre et leur présence sont importants et ne doivent pas être changés.

Cela implique que chaque nouveau fichier ajouté dans ce dossier respecte ce format.

### Cardio rénale

Ces fichiers n'ont pas encore été ajouter au projet
