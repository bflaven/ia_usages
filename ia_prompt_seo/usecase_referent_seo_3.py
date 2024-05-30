"""
[env]
# Conda Environment
conda create --name fmm_fastapi_poc python=3.9.13
conda info --envs
source activate fmm_fastapi_poc
conda deactivate

# if needed to remove
conda env remove -n [NAME_OF_THE_CONDA_ENVIRONMENT]
conda env remove -n fmm_fastapi_poc


# update conda 
conda update -n base -c defaults conda

# to export requirements
pip freeze > requirements.txt

# to install
pip install -r requirements.txt

# manual install
To complete

# [path]
cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_prompt_seo


# launch the file
python usecase_referent_seo_3.py



"""

# for api key
import os
from dotenv import load_dotenv

# Import the OpenAI class from the openai module
from openai import OpenAI

### 1. GET API KEY ###
# Load environment variables from the .env file
load_dotenv()

# Access the API key using os.getenv
api_key = os.getenv("OPENAI_API_KEY")


### 2. GET STUFF FROM CHATGPOT ###
# Create an instance of the OpenAI class with the provided API key
client = OpenAI(api_key=api_key)

def openai_chat(user_prompt):

    # Create a chat completion using the OpenAI client
    response = client.chat.completions.create(
        # Set the model to "gpt-3.5-turbo-0125"
        model="gpt-3.5-turbo-0125", 
        messages=[{"role": "user", "content": user_prompt}]
    )

    # Response from the chat completion
    answer = response.choices[0].message.content

    # Calculate the price for input tokens
    # For gpt-3.5-turbo-0125
    # Input : 0,50 US$ / 1M tokens
    
    input_price = response.usage.prompt_tokens * (0.5 / 1e6)

    # Calculate the price for output tokens
    # For gpt-3.5-turbo-0125
    # Output : 1,50 US$ / 1M tokens

    output_price = response.usage.completion_tokens * (1.5 / 1e6)

    # calculate the total price
    total_price = input_price + output_price

    # Return the answer, input price, output price, total price
    return {
        "answer": answer,
        "input_price": f"$ {input_price}",
        "output_price": f"$ {output_price}",
        "total_price": f"$ {total_price}"
    }
### 3. USING CLASS  ###
class MyOpenAI:

    ############## INITIALIZATION ##############
    def __init__(self, api_key: str, model_name: str = 'gpt-3.5-turbo-0125', vision_model_name: str = 'gpt-4-turbo'):
        """
        Initializes the OpenAILingua class with the provided API key and model names (optional).

        Args:
            api_key (str): A string representing the API key for the Generative AI model.
            model_name (str): If not provided, the default value is 'gpt-3.5-turbo-0125'.
            vision_model_name (str): If not provided, the default value is 'gpt-4-turbo'.
        """

        # Configuring Generative AI with API key
        self.client = OpenAI(api_key=api_key)

        # text generation model
        self.model_name = model_name

        # vision model
        self.vision_model_name = vision_model_name

    ############## TRANSLATE TEXT ##############

    def text_translate(self, user_input: str, target_lang: str) -> str:
        """
        Translates the given input text into the target language.

        Example:
        >>> text_translate("Farid khan and asad are coming to my house at 5 pm", "urdu")
        'فرید خان اور اسد شام 5 بجے میرے گھر آ رہے ہیں'

        Args:
            user_input (str): A string representing the input sentence.
            target_lang (str): A string representing the target language to translate the input into.

        Returns:
            str: A string representing the translated text.
        """

        # Generate the prompt template
        prompt_template = f'''
        Given the input text:
        user input: {user_input}

        convert it into {target_lang} language
        output must contain only the translated text
        '''

        # check if parameters are of correct type
        if not isinstance(user_input, str):
            raise TypeError("user_input must be of type str")
        if not isinstance(target_lang, str):
            raise TypeError("target_lang must be of type str")

        # check if parameters are not empty
        if not user_input:
            raise ValueError("user_input cannot be empty")
        if not target_lang:
            raise ValueError("target_lang cannot be empty")

        try:
            # Generate response using the provided model (assuming it's defined elsewhere)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt_template}],
            )
            response1 = response.choices[0].message.content
            return response1
        except Exception as e:
            return "Translation failed. Only the most popular languages are supported. Actively working to add more."


### 4. RESULT CLASS  ###

openai_model = MyOpenAI(api_key=api_key)


# 2. Text Translate
user_input = """As the sunset painted the sky with shades of orange and pink, a gentle breeze rustled the leaves, creating a soothing symphony, while the aroma of freshly brewed coffee filled the cozy cafe."""
openai_translation = openai_model.text_translate(user_input, target_lang="french")
print("OpenAI Translation:", openai_translation)



