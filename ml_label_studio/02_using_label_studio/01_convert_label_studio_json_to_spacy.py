#!/usr/bin/python
# -*- coding: utf-8 -*-
#

"""
[env]
# Conda Environment
conda create --name ml_with_label_studio python=3.9.13
conda info --envs
source activate ml_with_label_studio

conda deactivate
# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]

# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements_using_label_studio.txt



# to install
pip install -r requirements_using_label_studio.txt

# [path]
cd /Users/brunoflaven/Documents/01_work/blog_articles/ml_label_studio/02_using_label_studio/

python 01_convert_label_studio_json_to_spacy.py


In python, can you with a parser with the function data = json.load(f)
that loop through the object named "annotations":[] and print the values: start, end,labels and also print the value text from data from the following json named "export_2_labelstud_johnidm_reduce.json" that is available below.


In python, can you modify the same script and add a loop for value = annotation["result"][0]["value"] because it is not only with the indices equal to [0]. There are several values e.g  annotation["result"][0]["value"], annotation["result"][1]["value"], annotation["result"][3]["value"]... etc as the object can be a list, can you loop through the lits in the same script?


In python, can you modify the same script to output the result of the script inside a file named "spacy_output_format.json" in an object e.g [] make sure that the last value annotation["result"][n]["value"] has not commer at the end as it is the last value from the object. The file structure for "spacy_output_format.json" should be like below:




[
  [
    "text_data_1",
    {
      "entities":[
        [
          start,
          end,
          "labels"
        ]
      ]
    }
  ],
  [
    "text_data_2",
    {
      "entities":[
        [
          start,
          end,
          "labels"
        ]
      ]
    }
  ]
]


In this python script, when the script is exporting to a file named "spacy_output_format.json" be sure to introduce a decode("utf-8")) because if the language is not english, you may get characters like \u00e7 or \u00e1...
"""
 



# Top load JSON data required the package
import json


# SET THE VALUES
INPUTFILE_LABEL_STUDIO_EXPORT_JSON = 'label_studio_export_json_ner/example_2_project-6-at-2023-07-27-11-27-d2025d2a.json'

OUPUTFILE_SPACY_JSON = "spacy_output_format_crypto.json"

with open(INPUTFILE_LABEL_STUDIO_EXPORT_JSON, 'r') as f:

    # Parse JSON data
    data = json.load(f)

    output_list = []

    # Loop through each item in the JSON array
    for item in data:
        annotations = item["annotations"]
        text_data = item["data"]["text"]

        entities = []
        for annotation in annotations:
            results = annotation["result"]
            for result in results:
                try:
                    value = result["value"]
                    start = value["start"]
                    end = value["end"]
                    
                    # V0
                    # labels = value["labels"]
                    # print(labels)
                    
                    #V1
                    # Convert labels list to a comma-separated string
                    labels = ",".join(value["labels"])
                    # print(labels)
                    
                    entities.append([start, end, labels])

                except (KeyError, IndexError):
                    print("Error: Invalid 'value' in the annotation result.")

        output_list.append([text_data, {"entities": entities}])

    # Write the output_list to the "spacy_output_format.json" file with UTF-8 encoding
    with open(OUPUTFILE_SPACY_JSON, "w", encoding="utf-8") as outfile:
        json.dump(output_list, outfile, indent=2, ensure_ascii=False)

    print(f'Output has been written to {OUPUTFILE_SPACY_JSON} successfully.')
