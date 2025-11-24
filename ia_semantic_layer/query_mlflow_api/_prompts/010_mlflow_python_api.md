
## PROMPT
As a Python and MLflow expert, can you write a script that do the following:
1. The script parses each run inside the `"runs": []` object that exists in the output file created e.g `bf-auto-batch-20251105-134413.json`. I should be able to update the name of the output file created easily so so put it in  available at the top of the script.
2. The script take the value inisde `output` that should a correct json output. See below in `good output example for a run` and output each item for the CSV with the following columns: `title`, `summary`, `keywords`, `supertag`.
3. Here the values for the CSV : 
The value "1" is `title`
The value "2" is `summary`
The value "3" is `keywords`
The value "4" is `supertag`.


**good output example for a run**
```json
{
    "1": "Fayski Piegon court vers la barrière des 4 minutes du mile",
    "2": "Le jeudi prochain, le triple championne olympique en titre Fayski Piegon tentera de descendre sa propre marque de près de huit secondes pour passer la mythique barrière des 4 minutes sur le mile. Le projet est un vrai coup marketing pour la marque à la virgule qui mettra en avant ses produits. Il y aura une rencontre face aux émiratis d'Alaïne et l'événement sera ouvert au public avec un programme prévu. On peut se demander si Fayski Piegon réussira à établir son nouveau record, ou s'il pourra être victime des pressions de cette compétition. En plus de cela, le succès de l'athlète poursuit-il sa collaboration avec Solène Ravenel ?",
    "3": [
        "Fayski Piegon",
        "records",
        "mile",
        "barrière 4 minutes",
        "Solène Ravenel"
    ],
    "4": "Athlétisme"
}
```





## OUTPUT
See 0010_mlflow_python_api.py








