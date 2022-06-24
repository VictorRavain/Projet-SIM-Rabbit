# Projet-SIM-Rabbit
Projet visant à développer un automate simulant les fonctions vitales d'un lapin


Les fichiers de données : 

On considère deux types donnée: cardio-respiratoire et cardio-rénale. 

Une séance de TP est découpée en plusieurs fichiers de texte, un par séquence. Chaque fichier porte le nom de la séquence et est compressé au format lzma. Le séparateur est la tabulation (\t). Une séquence correspond à un état de l'animal et reporte l'évolution de différentes constantes au cours du temps. Par exemple, un fichier nommé Sansinjection.txt.lzma est un fichier compressé décrivant différentes constantes alors que l'animal n'a encore subit aucune injection. A l'inverse, Adrenaline.txt.lzma reporte l'évolution, avec le temps, des différentes constantes enregistrées suite à l'injection d'adrenaline.

Cardio réspiratoire
Les fichiers se trouvent dans ./public/data/Cardio_Respi/ et sont classés en sous-dossiers.


Par convention, les fichiers de ce dossier ont le format suivant:

Time        PA          SP  PA moy.     FC          FR
1350,05     1280,039    0   1169,866    154,7285    20,66807
1350,051    1280,039    0   1169,866    154,7285    20,66807
1350,052    1280,039    0   1169,866    154,7285    20,66807
...


L'en-tête doit être présente mais est ignoré lors du chargement du fichier. Les colonnes sont les suivantes:

Time : horodatage de la ligne (il y a une ligne toutes les 5ms).
PA : Pression Artérielle
SP : Spirometrie
PA moy. : PA moyenne
FC : Fréquence Cardiaque
FR : Fréquence Respiratoire
L'ordre et leur présence sont importants et ne doivent pas être changés.

Cela implique que chaque nouveau fichier ajouté dans ce dossier respecte ce format.



Cardio rénale
Les fichiers cardio-rénale n'ont pas encore été ajouter à la base de de donnée
