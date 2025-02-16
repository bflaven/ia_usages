
# 010_ia_kpi_llm.md


## PROMPT_1

<!-- 
Faire le bilan énergétique de chaque usage de l'IA avec aussi le cout financier
 -->
<!-- 
ex : consommation énergétique, émissions de CO2
Comprendre la classe énergétique de sa maison | MaisonSûr
https://www.maisonsur.com/blog/trucs-astuces/comprendre-la-classe-energetique-de-sa-maison/
classe enérgetiquen dépense d'une maison de 100m2

-->


Donner les niveaux du tableau de la classe énergétique de sa maison "consomation enérgetique", "performance de la maison"



 

```text

```

## CLAUDE_1

Je vais créer une représentation visuelle du tableau des classes énergétiques (DPE - Diagnostic de Performance Énergétique) pour les logements.



Ce tableau présente les différentes classes énergétiques des logements en France :

- Classe A (très performant) : Consommation ≤ 70 kWh/m²/an
- Classe B (performant) : Consommation entre 71 et 110 kWh/m²/an
- Classe C (assez performant) : Consommation entre 111 et 180 kWh/m²/an
- Classe D (assez peu performant) : Consommation entre 181 et 250 kWh/m²/an
- Classe E (peu performant) : Consommation entre 251 et 330 kWh/m²/an
- Classe F (très peu performant) : Consommation entre 331 et 420 kWh/m²/an
- Classe G (extrêmement peu performant) : Consommation > 420 kWh/m²/an

Ces valeurs sont exprimées en kilowattheures d'énergie primaire par mètre carré et par an (kWh/m²/an). Plus la classe est proche de A, plus le logement est performant énergétiquement et moins il consomme d'énergie.

```javascript
import React from 'react';

const DPETableau = () => {
  const classes = [
    { niveau: 'A', conso: '≤ 70', couleur: 'bg-green-500' },
    { niveau: 'B', conso: '71 à 110', couleur: 'bg-green-400' },
    { niveau: 'C', conso: '111 à 180', couleur: 'bg-green-300' },
    { niveau: 'D', conso: '181 à 250', couleur: 'bg-yellow-300' },
    { niveau: 'E', conso: '251 à 330', couleur: 'bg-orange-400' },
    { niveau: 'F', conso: '331 à 420', couleur: 'bg-red-400' },
    { niveau: 'G', conso: '> 420', couleur: 'bg-red-600' }
  ];

  return (
    <div className="w-full max-w-2xl p-4">
      <h2 className="text-xl font-bold mb-4">Diagnostic de Performance Énergétique (DPE)</h2>
      <div className="border rounded-lg overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="py-2 px-4 text-left">Classe</th>
              <th className="py-2 px-4 text-left">Consommation</th>
              <th className="py-2 px-4 text-left">Unité</th>
            </tr>
          </thead>
          <tbody>
            {classes.map((classe, index) => (
              <tr key={classe.niveau} className={`${classe.couleur} text-white`}>
                <td className="py-2 px-4 font-bold">{classe.niveau}</td>
                <td className="py-2 px-4">{classe.conso}</td>
                <td className="py-2 px-4">kWh/m²/an</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-4 text-sm text-gray-600">
        * Les valeurs sont exprimées en kWh d'énergie primaire par m² et par an
      </p>
    </div>
  );
};

export default DPETableau;
```


```html

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">
    <!-- Title -->
    <text x="400" y="40" text-anchor="middle" font-size="24" font-weight="bold" fill="#333">
        Diagnostic de Performance Énergétique (DPE)
    </text>
    
    <!-- Legend -->
    <text x="50" y="80" font-size="14" fill="#666">
        Logement économe
    </text>
    <text x="50" y="440" font-size="14" fill="#666">
        Logement énergivore
    </text>

    <!-- Energy Levels -->
    <g transform="translate(50, 100)">
        <!-- A -->
        <rect x="0" y="0" width="600" height="40" fill="#319834"/>
        <text x="20" y="27" fill="white" font-size="20" font-weight="bold">A</text>
        <text x="60" y="27" fill="white" font-size="18">≤ 70</text>
        <text x="520" y="27" fill="white" font-size="14">kWh/m²/an</text>

        <!-- B -->
        <rect x="0" y="45" width="600" height="40" fill="#33cc31"/>
        <text x="20" y="72" fill="white" font-size="20" font-weight="bold">B</text>
        <text x="60" y="72" fill="white" font-size="18">71 à 110</text>
        <text x="520" y="72" fill="white" font-size="14">kWh/m²/an</text>

        <!-- C -->
        <rect x="0" y="90" width="600" height="40" fill="#cdfd33"/>
        <text x="20" y="117" fill="black" font-size="20" font-weight="bold">C</text>
        <text x="60" y="117" fill="black" font-size="18">111 à 180</text>
        <text x="520" y="117" fill="black" font-size="14">kWh/m²/an</text>

        <!-- D -->
        <rect x="0" y="135" width="600" height="40" fill="#ffd733"/>
        <text x="20" y="162" fill="black" font-size="20" font-weight="bold">D</text>
        <text x="60" y="162" fill="black" font-size="18">181 à 250</text>
        <text x="520" y="162" fill="black" font-size="14">kWh/m²/an</text>

        <!-- E -->
        <rect x="0" y="180" width="600" height="40" fill="#ffa733"/>
        <text x="20" y="207" fill="white" font-size="20" font-weight="bold">E</text>
        <text x="60" y="207" fill="white" font-size="18">251 à 330</text>
        <text x="520" y="207" fill="white" font-size="14">kWh/m²/an</text>

        <!-- F -->
        <rect x="0" y="225" width="600" height="40" fill="#ff7433"/>
        <text x="20" y="252" fill="white" font-size="20" font-weight="bold">F</text>
        <text x="60" y="252" fill="white" font-size="18">331 à 420</text>
        <text x="520" y="252" fill="white" font-size="14">kWh/m²/an</text>

        <!-- G -->
        <rect x="0" y="270" width="600" height="40" fill="#ff0000"/>
        <text x="20" y="297" fill="white" font-size="20" font-weight="bold">G</text>
        <text x="60" y="297" fill="white" font-size="18">> 420</text>
        <text x="520" y="297" fill="white" font-size="14">kWh/m²/an</text>
    </g>

    <!-- Footer Note -->
    <text x="50" y="470" font-size="12" fill="#666">
        * Les valeurs sont exprimées en kWh d'énergie primaire par m² et par an
    </text>
</svg>





```