
## PROMPT
As a Python and MLflow expert, keep the script as it is as it is working but can you use .env to externalize the following values. 

```python
MLFLOW_TRACKING_URI
USERNAME
PASSWORD
MLFLOW_DEPLOYMENTS_TARGET
GATEWAY_ENDPOINT_NAME
EXPERIMENT_NAME
INPUT_JSON_FILE
PROMPT_TEMPLATE
MODEL_NAME
TEMPERATURE
MAX_TOKENS
```

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
[check]
pip --version
python --version

[env]
Recommended: Use Built-in venv

Create a new environment:
python -m venv mlflow_python_api

Activate the environment:
source mlflow_python_api/bin/activate

Install packages inside the environment:
pip install package_name

pip install mlflow
pip install mlflow==3.3.1
pip install requests
python -m pip install mlflow==3.3.1

python -m pip install --upgrade pip setuptools wheel

brew install cmake
brew install apache-arrow
export CMAKE_PREFIX_PATH=$(brew --prefix apache-arrow)/lib/cmake


Deactivate:
deactivate

To easily reproduce environments:
pip freeze > requirements.txt

Install everything in a new environment:
pip install -r requirements.txt


# [path]
cd /Users/brunoflaven/Documents/02_copy/_strategy_IA_fmm/mlflow_python_api/

# LAUNCH the file
python 0009_mlflow_python_api.py


MLflow Run Creation Script with MLflow Gateway/Deployments
Creates a run inside a specified MLflow experiment and calls the LLM model
through MLflow Gateway/Deployments using chat format.

MLflow Version: 3.3.1
Author: Generated for Bruno Flaven
Date: November 2025
"""

import mlflow
from mlflow.tracking import MlflowClient
from mlflow.deployments import get_deploy_client
import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MLflowLLMRunner:
    """
    Class to handle MLflow run creation with MLflow Gateway/Deployments inference
    """
    
    def __init__(self, tracking_uri: str, username: str, password: str, deployments_target: str):
        """
        Initialize the MLflow client with authentication
        
        Args:
            tracking_uri: The MLflow tracking server URL
            username: HTTP Basic Auth username
            password: HTTP Basic Auth password
            deployments_target: MLflow Gateway/Deployments target URL
        """
        self.tracking_uri = tracking_uri
        self.username = username
        self.password = password
        self.deployments_target = deployments_target
        self._setup_authentication()
        self.client = None
        self.deploy_client = None
        
    def _setup_authentication(self):
        """
        Set up authentication credentials in environment variables
        MLflow uses these for HTTP Basic Authentication
        """
        # Set authentication credentials as environment variables
        os.environ['MLFLOW_TRACKING_USERNAME'] = self.username
        os.environ['MLFLOW_TRACKING_PASSWORD'] = self.password
        
        # Set the tracking URI
        mlflow.set_tracking_uri(self.tracking_uri)
        
        # Set deployments target
        os.environ['MLFLOW_DEPLOYMENTS_TARGET'] = self.deployments_target
        
        logger.info(f"Configured MLflow tracking URI: {self.tracking_uri}")
        logger.info(f"Configured MLflow deployments target: {self.deployments_target}")
        logger.info(f"Authentication credentials set for user: {self.username}")
        
    def initialize_client(self):
        """
        Initialize the MLflow tracking client
        """
        try:
            self.client = MlflowClient()
            logger.info("MLflow tracking client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MLflow client: {e}")
            return False
    
    def initialize_deploy_client(self):
        """
        Initialize the MLflow deployments client
        """
        try:
            self.deploy_client = get_deploy_client(self.deployments_target)
            logger.info("MLflow deployments client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MLflow deployments client: {e}")
            return False
    
    def get_experiment_by_name(self, experiment_name: str):
        """
        Get experiment by name
        
        Args:
            experiment_name: Name of the experiment
            
        Returns:
            Experiment object or None if not found
        """
        try:
            experiment = self.client.get_experiment_by_name(experiment_name)
            if experiment:
                logger.info(f"Found experiment: {experiment_name} (ID: {experiment.experiment_id})")
                return experiment
            else:
                logger.error(f"Experiment '{experiment_name}' not found")
                return None
        except Exception as e:
            logger.error(f"Error getting experiment: {e}")
            return None
    
    def replace_template_variables(self, prompt_template: str, variables: Dict[str, str]) -> str:
        """
        Replace template variables in prompt with actual values
        
        Args:
            prompt_template: Prompt template with {{ variable }} placeholders
            variables: Dictionary of variable names and their values
            
        Returns:
            Processed prompt with variables replaced
        """
        processed_prompt = prompt_template
        for var_name, var_value in variables.items():
            placeholder = f"{{{{ {var_name} }}}}"
            processed_prompt = processed_prompt.replace(placeholder, var_value)
        
        logger.info(f"Processed prompt length: {len(processed_prompt)} characters")
        return processed_prompt
    
    def call_gateway_model(
        self,
        endpoint_name: str,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 20000
    ) -> Dict[str, Any]:
        """
        Call MLflow Gateway/Deployments model to generate response using chat format
        
        Args:
            endpoint_name: Name of the gateway endpoint/route
            prompt: The prompt to send to the model
            temperature: Temperature parameter for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            Dictionary with model response and metadata
        """
        try:
            logger.info(f"Calling MLflow Gateway endpoint: {endpoint_name}")
            logger.info(f"Gateway target: {self.deployments_target}")
            
            # Use CHAT format (messages) as expected by the gateway
            inputs = {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            logger.info(f"Sending payload with prompt length: {len(prompt)}")
            
            # Call the gateway endpoint
            response = self.deploy_client.predict(
                endpoint=endpoint_name,
                inputs=inputs
            )
            
            logger.info(f"Response type: {type(response)}")
            
            # Extract output based on response format
            output_text = ""
            
            if isinstance(response, dict):
                logger.info(f"Response keys: {response.keys()}")
                
                if 'choices' in response and len(response['choices']) > 0:
                    first_choice = response['choices'][0]
                    
                    if 'message' in first_choice:
                        message = first_choice['message']
                        output_text = message.get('content', '')
                    elif 'text' in first_choice:
                        output_text = first_choice['text']
                    elif 'content' in first_choice:
                        output_text = first_choice['content']
                    else:
                        logger.warning(f"Unknown choice format: {first_choice}")
                        output_text = str(first_choice)
                
                elif 'response' in response:
                    output_text = response['response']
                
                elif 'message' in response:
                    if isinstance(response['message'], dict):
                        output_text = response['message'].get('content', str(response['message']))
                    else:
                        output_text = str(response['message'])
                
                elif 'predictions' in response:
                    predictions = response['predictions']
                    output_text = predictions[0] if isinstance(predictions, list) and predictions else str(predictions)
                elif 'text' in response:
                    output_text = response['text']
                elif 'output' in response:
                    output_text = response['output']
                elif 'content' in response:
                    output_text = response['content']
                else:
                    logger.warning(f"Unknown response format, dumping entire response")
                    output_text = json.dumps(response)
                    
            elif isinstance(response, str):
                output_text = response
            elif isinstance(response, list) and len(response) > 0:
                output_text = str(response[0])
            else:
                output_text = str(response)
            
            logger.info(f"Extracted output text length: {len(output_text)} characters")
            
            return {
                "success": True,
                "output": output_text,
                "raw_response": response
            }
            
        except Exception as e:
            logger.error(f"Error calling MLflow Gateway: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "output": None
            }
    
    def create_run_with_llm_inference(
        self,
        experiment_name: str,
        run_name: str,
        prompt_template: str,
        prompt_variables: Dict[str, str],
        model_name: str,
        endpoint_name: str,
        temperature: float,
        max_tokens: int,
        additional_params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a new run in the specified experiment with Gateway model inference
        
        Args:
            experiment_name: Name of the experiment
            run_name: Name for the run
            prompt_template: Prompt template with variables
            prompt_variables: Dictionary of variables to replace in template
            model_name: Name of the model (for logging)
            endpoint_name: Name of the gateway endpoint/route
            temperature: Temperature parameter for model
            max_tokens: Maximum tokens for model response
            additional_params: Additional parameters to log
            
        Returns:
            Dictionary with run information and results
        """
        # Get the experiment
        experiment = self.get_experiment_by_name(experiment_name)
        if not experiment:
            logger.error(f"Cannot create run: experiment '{experiment_name}' not found")
            return None
        
        # Process the prompt template
        processed_prompt = self.replace_template_variables(prompt_template, prompt_variables)
        
        # Call the Gateway model
        logger.info("Calling MLflow Gateway to generate output...")
        llm_response = self.call_gateway_model(
            endpoint_name=endpoint_name,
            prompt=processed_prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        if not llm_response.get('success'):
            logger.error(f"LLM inference failed: {llm_response.get('error')}")
            return None
        
        output = llm_response.get('output', '')
        
        # Ensure output is not empty
        if not output or output.strip() == "":
            logger.error("LLM returned empty output!")
            logger.error(f"Raw response was: {llm_response.get('raw_response')}")
            return None
        
        try:
            # Start a new MLflow run
            with mlflow.start_run(
                experiment_id=experiment.experiment_id,
                run_name=run_name
            ) as run:
                
                # Log the prompt template
                mlflow.log_param("prompt_template", prompt_template[:250])  # Truncate if too long
                
                # Log prompt variables individually
                for var_name, var_value in prompt_variables.items():
                    # Truncate long values for param logging
                    if len(str(var_value)) > 250:
                        mlflow.log_param(var_name, str(var_value)[:250] + "...")
                    else:
                        mlflow.log_param(var_name, var_value)
                
                # Log model parameters
                mlflow.log_param("model_name", model_name)
                mlflow.log_param("temperature", temperature)
                mlflow.log_param("max_tokens", max_tokens)
                
                # Log the output - truncate if too long for param
                if len(output) > 250:
                    mlflow.log_param("output", output[:250] + "...")
                else:
                    mlflow.log_param("output", output)
                
                # Log additional parameters if provided
                if additional_params:
                    for key, value in additional_params.items():
                        mlflow.log_param(key, value)
                
                # Prepare run information
                run_info = {
                    "run_id": run.info.run_id,
                    "run_name": run_name,
                    "experiment_id": experiment.experiment_id,
                    "experiment_name": experiment_name,
                    "prompt_template": prompt_template,
                    "prompt_variables": prompt_variables,
                    "processed_prompt": processed_prompt,
                    "model_name": model_name,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "output": output,
                    "timestamp": datetime.now().isoformat(),
                    "status": "completed"
                }
                
                logger.info(f"Run created successfully: {run.info.run_id}")
                logger.info(f"Run name: {run_name}")
                logger.info(f"Experiment: {experiment_name}")
                
                return run_info
                
        except Exception as e:
            logger.error(f"Error creating run: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_runs_to_json(self, runs_info: List[Dict[str, Any]], output_file: str):
        """
        Save multiple run information to a JSON file
        
        Args:
            runs_info: List of dictionaries containing run information
            output_file: Output JSON file path
        """
        try:
            output_data = {
                "total_runs": len(runs_info),
                "timestamp": datetime.now().isoformat(),
                "runs": runs_info
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Run information saved to {output_file}")
            print(f"\n✓ Run data exported to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving runs to JSON: {e}")


def load_gold_dataset(json_file: str) -> List[Dict[str, Any]]:
    """
    Load the gold dataset from JSON file
    
    Args:
        json_file: Path to the JSON file containing gold_dataset
        
    Returns:
        List of dataset items
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'gold_dataset' not in data:
            logger.error(f"JSON file does not contain 'gold_dataset' key")
            return []
        
        dataset = data['gold_dataset']
        logger.info(f"Loaded {len(dataset)} items from {json_file}")
        return dataset
        
    except FileNotFoundError:
        logger.error(f"JSON file not found: {json_file}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file: {e}")
        return []
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return []


def generate_timestamp() -> str:
    """
    Generate timestamp in format: YYYYMMDD-HHMMSS
    """
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def main():
    """
    Main function to create MLflow runs with Gateway model inference for each item in gold_dataset
    """
    
    # ============================================================================
    # CONFIGURATION - Modify these values for different runs
    # ============================================================================
    
    # MLflow Server Configuration
    MLFLOW_TRACKING_URI = "[site]/mlflow"
    USERNAME = "[username]"
    PASSWORD = "[password]"
    
    # MLflow Gateway/Deployments Configuration
    MLFLOW_DEPLOYMENTS_TARGET = "[site]/mlflow_gateway"
    
    # Gateway Endpoint/Route Name (chat endpoint)
    GATEWAY_ENDPOINT_NAME = "mistral-ollama"
    
    # Experiment Selection
    EXPERIMENT_NAME = "gold_dataset"
    
    # Input JSON file with gold_dataset
    INPUT_JSON_FILE = "gold_dataset_api_mlflow_full_2.json"
    
    # Prompt Template Configuration
    PROMPT_TEMPLATE = """
    En vous inspirant des exemples de titres suivants et en adoptant le profil d'un journaliste expérimenté spécialisé dans l'actualité internationale, générez un objet JSON valide strictement conforme aux spécifications ci-dessous à partir du texte suivant : 

{{ content }}

Le journaliste est un professionnel rigoureux, doté d'un sens aigu de l'éthique et d'une grande curiosité pour les affaires mondiales. Il est connu pour sa capacité à rendre accessibles des sujets complexes, tout en respectant les nuances culturelles et politiques. Aucune balise de code ou formatage supplémentaire n'est autorisée. La sortie doit être un objet JSON strict pouvant être consommé directement par une API, sans texte explicatif, sans balises ou tout autre format additionnel.

Lorsque le contenu aborde plusieurs thématiques, choisissez celle qui est le plus largement développée dans le contenu. Développez une problématique sur cette thématique principale.

Exemples de titres :
1. Japon : le combat des pères pour la garde partagée
2. Le successeur du Dalaï-lama sera désigné après sa mort, la Chine veut approuver son nom
3. Ibn Battuta, l'explorateur marocain qui "fait passer Marco Polo pour un flemmard"
4. DJ Snake et Omar Sy dévoilent "Patience", l'épopée "universelle" d'un jeune exilé sénégalais
5. Trump a-t-il raison de dire que l'article 5 de l'Otan peut "s'interpréter de plusieurs façons" ?
6. Washington cesse de livrer certaines armes à l'Ukraine, Kiev convoque le chargé d'affaires américain
7. Emmanuel Grégoire, le socialiste qui rêve de succéder à Anne Hidalgo à Paris
8. Fuites, pollutions, prix… En Outre-mer, une "discrimination environnementale" dans l'accès à l'eau

Format attendu du JSON :
1. "1" : Un titre en {{ lang }} journalistique créatif, pertinent, engageant, riche en mots-clés et adapté à une diffusion sur internet et les réseaux sociaux, pour un média d'actualité internationale. Le titre doit être rédigé en {{ lang }} et respecter les règles typographiques de la presse en {{ lang }} : seule la première lettre du titre doit être en majuscule, les autres lettres en minuscules (sauf noms propres). Les titres doivent comporter entre 50 et 60 caractères (espaces compris). Le titre peut contenir une touche d'humour, mais doit toujours refléter fidèlement le contenu, sans sensationnalisme. Puisqu'il traite de l'actualité internationale, les indications de pays ou de régions sont à privilégier dans les mots-clés de ces titres.
2. "2" : Un résumé complet en {{ lang }} et concis de 8 à 10 phrases des points principaux du texte, avec 1 ou 2 mots-clés inclus pour susciter l'intérêt du lecteur. Ce résumé doit faire entre 600 et 1000 caractères, avec une préférence pour 800 caractères. Il doit résumer la thématique principale en développant une problématique sur cette thématique, sans dévoiler tous les détails, afin de susciter l'intérêt du lecteur, mettre en avant l'angle principal de l'article, en étant à la fois informatif et incitatif. Adopter un ton professionnel, clair, structuré, précis et pédagogique, adapté à un grand public exigeant. Intégrer, si pertinent, une citation ou un chiffre marquant tiré du texte, pour renforcer l'accroche et l'intérêt du chapeau. Citez ensuite les autres sujets ou thématiques secondaires en les distinguant bien de la première thématique. Pour accroître la pertinence sur la thématique principale, posez une ou deux questions rhétoriques qui invitent le lecteur à réfléchir davantage sur le sujet principal. Abordez les thématiques secondaires sous forme de questions pour susciter la curiosité du lecteur et l'inciter à lire l'article complet.
3. "3" : Un tableau de quatre à sept mots-clés ou expressions les plus pertinents du texte, que les lecteurs potentiels utiliseraient pour le rechercher. Ces mots-clés doivent être en {{ lang }}.
4. "4" : Une catégorie unique en {{ lang }} à laquelle appartient le contenu, en utilisant strictement les catégories suivantes : {{ cms_section_keywords_list }}. La catégorie doit être en {{ lang }} et refléter la localisation géographique ou la thématique principale du contenu.

Le résultat doit être en {{ lang }} et structuré en JSON strictement comme suit :
{
  "1": "Titre de l'article 1",
  "2": "Résumé de l'article en 8-10 phrases.",
  "3": ["Mot-clé 1", "Mot-clé 2", "Mot-clé 3", "Mot-clé 4", "Mot-clé 5"],
  "4": "Catégorie ou sujet principal"
}

Assurez-vous que la catégorie choisie dans le champ 4 est bien dans la langue c'est à dire en {{ lang }} et que le format de sortie est strictement respecté. Ne fournissez que l'objet JSON pur en {{ lang }}, sans aucune balise, texte explicatif, ou autre formatage non JSON. Le résultat doit être un JSON brut et valide, strictement conforme aux spécifications, prêt à être consommé par une API.
    """
    
    # LLM Model Configuration
    MODEL_NAME = "mistral-ollama"
    TEMPERATURE = 0.8
    MAX_TOKENS = 30000
    
    # Run Name Base (timestamp will be added for each run)
    timestamp = generate_timestamp()
    OUTPUT_JSON_FILE = f"bf-auto-batch-{timestamp}.json"
    
    # Additional Parameters (optional)
    ADDITIONAL_PARAMS = {
        "created_by": "python_script_batch",
        "purpose": "prompt_testing_batch"
    }
    
    # ============================================================================
    # END CONFIGURATION
    # ============================================================================
    
    print("="*80)
    print("MLflow LLM Runner - Batch Processing with Gateway/Deployments")
    print("="*80)
    print(f"MLflow Version: {mlflow.__version__}")
    print(f"Tracking URI: {MLFLOW_TRACKING_URI}")
    print(f"Deployments Target: {MLFLOW_DEPLOYMENTS_TARGET}")
    print(f"Gateway Endpoint: {GATEWAY_ENDPOINT_NAME}")
    print(f"Experiment: {EXPERIMENT_NAME}")
    print(f"Input JSON: {INPUT_JSON_FILE}")
    print("="*80)
    
    # Load the gold dataset
    print(f"\n[1] Loading gold dataset from {INPUT_JSON_FILE}...")
    gold_dataset = load_gold_dataset(INPUT_JSON_FILE)
    
    if not gold_dataset:
        logger.error("No data to process. Exiting.")
        sys.exit(1)
    
    print(f"✓ Loaded {len(gold_dataset)} items from dataset")
    
    # Initialize the runner with credentials
    runner = MLflowLLMRunner(
        tracking_uri=MLFLOW_TRACKING_URI,
        username=USERNAME,
        password=PASSWORD,
        deployments_target=MLFLOW_DEPLOYMENTS_TARGET
    )
    
    # Initialize tracking client
    if not runner.initialize_client():
        logger.error("Failed to initialize MLflow tracking client. Exiting.")
        sys.exit(1)
    
    # Initialize deployments client
    if not runner.initialize_deploy_client():
        logger.error("Failed to initialize MLflow deployments client. Exiting.")
        sys.exit(1)
    
    try:
        # List to collect all run information
        all_runs_info = []
        
        # Process each item in the gold dataset
        print(f"\n[2] Processing {len(gold_dataset)} items...")
        print("="*80)
        
        for index, item in enumerate(gold_dataset, start=1):
            print(f"\n{'='*80}")
            print(f"Processing item {index}/{len(gold_dataset)}")
            print(f"{'='*80}")
            print(f"Source: {item.get('source', 'N/A')}")
            
            # Extract values from the item
            lang = item.get('lang', '')
            cms_section_keywords_list = item.get('cms_section_keywords_list', '')
            content = item.get('content', '')
            source = item.get('source', f'item_{index}')
            
            # Create prompt variables for this item
            prompt_variables = {
                "content": content,
                "lang": lang,
                "cms_section_keywords_list": cms_section_keywords_list
            }
            
            # Generate unique run name for this item
            run_timestamp = generate_timestamp()
            run_name = f"bf-auto-{run_timestamp}"
            
            print(f"Run Name: {run_name}")
            print(f"Language: {lang}")
            print(f"Content length: {len(content)} characters")
            print("-"*80)
            
            # Create the run with LLM inference
            print(f"[{index}] Creating MLflow run with Gateway inference...")
            run_info = runner.create_run_with_llm_inference(
                experiment_name=EXPERIMENT_NAME,
                run_name=run_name,
                prompt_template=PROMPT_TEMPLATE,
                prompt_variables=prompt_variables,
                model_name=MODEL_NAME,
                endpoint_name=GATEWAY_ENDPOINT_NAME,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
                additional_params={**ADDITIONAL_PARAMS, "source": source, "item_index": index}
            )
            
            if run_info:
                # Add source information to run_info
                run_info['source'] = source
                run_info['item_index'] = index
                
                all_runs_info.append(run_info)
                
                print(f"✓ Run created successfully")
                print(f"  Run ID: {run_info['run_id']}")
                print(f"  Output length: {len(run_info['output'])} characters")
                print(f"  Output preview: {run_info['output'][:200]}...")
            else:
                logger.error(f"Failed to create run for item {index}")
                # Add failed run info
                all_runs_info.append({
                    "source": source,
                    "item_index": index,
                    "status": "failed",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Save all runs information to JSON
        print("\n" + "="*80)
        print(f"[3] Saving all {len(all_runs_info)} runs to JSON...")
        print("="*80)
        runner.save_runs_to_json(all_runs_info, OUTPUT_JSON_FILE)
        
        # Print summary
        successful_runs = sum(1 for r in all_runs_info if r.get('status') == 'completed')
        failed_runs = len(all_runs_info) - successful_runs
        
        print("\n" + "="*80)
        print("BATCH PROCESSING COMPLETE")
        print("="*80)
        print(f"Total items processed: {len(gold_dataset)}")
        print(f"Successful runs: {successful_runs}")
        print(f"Failed runs: {failed_runs}")
        print(f"Output file: {OUTPUT_JSON_FILE}")
        print(f"View your runs in MLflow UI at: {MLFLOW_TRACKING_URI}")
        print("="*80)
        
    except KeyboardInterrupt:
        print("\n\nScript interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
```



## OUTPUT
See 0010_mlflow_python_api.py








