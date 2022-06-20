# Comment gérer les fichiers

## Conditions pour ajouter un fichier dans le dossier `data` 

### Cardio_Respi
#### Pré-requis

1. Le fichier doit être nommé selon la séquence qu'il reporte suivi de l'extension `.txt`. 
*p-ex:* `Adrenaline.txt`
2. Son contenu doit respecter le format suivant:
    + 4 colonnes, dans l'ordre: 
        - CH1 spirométrie (amplitude ventilation) 
        - CH2 PA
        - CH40 Fréquence ventilatoire
        - CH41 Fréquence cardiaque 
    + les intitulés importent peu, ils seront ignorés, la lecture se basant sur l'ordre
    + chaque élement d'une ligne est séparé du suivant par une tabulation (`\t`) 
    + chaque ligne se termine par un retour chariot (`\n`)  
3. Le fichier texte est compréssé au format lzma: 
```bash 
$> lzma fichier.txt`
```
Ou pour convertir plusieurs fichiers en une commande:
```bash
for f in `find . -name "*.txt"`; do lzma $f; done
```

**Attention:**
il arrive parfois qu'un fichier ait été édité sous Windows et comporte des caractères `^M` en fin de ligne.
Pour éviter que certains éditeurs affichent ces valeurs, il convient de les supprimer:
```bash
cat fichier.txt | tr -d '\r' > fichier.txt
```




##### Exemple de contenu
```txt
CH1	CH2	CH40	CH41
-0.0167847	62.4634	19.0779	142.857
0.00152588	62.2559	19.0779	142.857
0.00915527	62.1216	19.0779	142.857
0.00305176	62.0972	19.0779	142.857
...
```    

#### Dépôt

1. Créer si nécessaire le sous-dossier correspondant à l'année du TP suivi de son nom. 
*p-ex:* `Data_2016/BlancheNeige`
2. Déposer le fichier dans le dossier, et l'ajouter à `git`