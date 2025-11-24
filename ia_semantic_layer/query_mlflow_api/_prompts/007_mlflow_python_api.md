
It does not record into mlflow and the script has degrated the output in the .json file. Can you fix the problem.



## PROMPT
As a Python and MLflow expert, the script is working so keep it as it but make the following modifications: 

1. Can you change the way you set variables like "OLD" and change it for the "NEW" version.
2. Enable this output in a json file but can the script also make a record of the result into the experiment with the values displayed in `run_name`, `output`, `text`, `word_count`, `lang`

Rewrite the entire script sio I can cut and paste

- NEW
```python
"text"="""
the text si coming here
"""
"word_count"="""
75
"""
"lang"="""
spanish
"""
```


- OLD
```python
# Prompt Variables (replace {{ variable_name }} in template)
    PROMPT_VARIABLES = {
            "text": "En una jornada electoral con implicaciones nacionales, los demócratas lograron victorias significativas en varios estados clave, destacando la elección de Zohran Mamdani como alcalde de Nueva York. Este candidato izquierdista se convierte en el primer musulmán en ocupar ese cargo. Con información de nuestro corresponsal en Washington, Cristóbal Vázquez. \"En este momento de oscuridad política, Nueva York será la luz\", declaró Mamdani durante su discurso de victoria en Brooklyn. Mamdani, legislador estatal de Nueva York por Queens, se autodenomina socialista e hizo campaña prometiendo reducir los costos de vida para los neoyorquinos de a pie. Nacido en Uganda en una familia de origen indio y naturalizado estadounidense, era virtualmente desconocido antes de ganar la nominación demócrata frente al exgobernador Andrew Cuomo. Victorias demócratas en Virginia y Nueva Jersey Además de Nueva York, los demócratas obtuvieron triunfos en Virginia y Nueva Jersey. En Virginia, Abigail Spanberger derrotó a la republicana Winsome Earle-Sears y asumirá como gobernadora. En Nueva Jersey, la veterana de la Marina Mikie Sherrill superó al empresario Jack Ciattarelli, consolidando otra victoria para el partido. En California, se aprobó la Proposición 50, que permitirá rediseñar el mapa electoral, con posibles efectos en el control del Congreso. El presidente Donald Trump reaccionó desde Truth Social, atribuyendo las derrotas republicanas a su ausencia en la boleta electoral y al reciente cierre del gobierno. \"El hecho de que no estuviera en el tarjetón y el cierre del gobierno fueron las dos principales razones por las cuales los republicanos perdieron las elecciones\", escribió. Figuras del mundo empresarial, incluyendo a Bill Ackman, atacaron ruidosamente a Mamdani y canalizaron dinero hacia sus rivales, mientras medios conservadores fueron críticos con sus declaraciones, entre otras, sobre el conflicto en Gaza entre Hamás e Israel.",
            "word_count": "75",
            "lang": "spanish",

    }

```







## OUTPUT
See 0008_mlflow_python_api.py








