import gradio
import argparse
# import rich
from typing import Dict, Any
from rich.console import Console
from transformers import pipeline

logger = Console(record=True)

# pre-load pipelines
xlm_roberta_base = pipeline('fill-mask', model='xlm-roberta-base')
logger.log(f"Loaded pipeline: [blue underline]xlm-roberta-base")
    
xlm_roberta_large = pipeline('fill-mask', model='xlm-roberta-large')
logger.log(f"Loaded pipeline: [blue underline]xlm-roberta-large")

# available mlm models
MODELS = [
    "xlm-roberta-base", 
    "xlm-roberta-large"
    ]

# set of examples for users to try out
examples = [
    ["Hello I'm a <mask> model."],
    # OUTPUT should be: Portland
    ["<mask> is the capital of Oregon"],
    # OUTPUT should be: Kampala
    ["<mask> is the capital and largest city of Uganda"],
    # OUTPUT should be: Ohio voters approve constitutional amendment that protects access to abortion
    # https://www.france24.com/en/americas/20231108-ohio-voters-approve-constitutional-amendment-that-protects-access-to-abortion
    ["Ohio <mask> approve constitutional amendment that protects access to abortion"],
    # OUTPUT should be: Record temperatures in October indicate 2023 will be warmest year in history
    # https://www.france24.com/en/environment/20231108-record-temperatures-in-october-guarantee-2023-will-be-warmest-year-in-history
    ["Record temperatures in October indicate 2023 will be <mask> year in history"],
    ["I love playing <mask>ball at the beach."],
    # OUTPUT should be: A French gay rights group said Wednesday it had launched legal action against Amazon Prime for offering on streaming replay a football match between Paris Saint-Germain and Marseille in which homophobic chants were audible.
    # https://www.france24.com/en/live-news/20231108-amazon-under-fire-over-homophobic-slurs-in-broadcast-of-psg-game
    ["A French gay rights group said Wednesday it had launched legal action against Amazon Prime for offering on streaming replay a football match between Paris Saint-Germain and Marseille in which <mask> chants were audible."]
    ]

def fill_mask(text: str, model: str) -> Dict:
    """ 
    Given a Masked Text, fills the masked token with suggestions from the Language Model.
    """
    suggestions = {}
    
    outputs = xlm_roberta_base(text) if model.endswith("base") else xlm_roberta_large(text)

    for output in outputs:
        suggestions[output["token_str"]] = output["score"] 

    return suggestions

def main(args: Any) -> None:
    # create gui
    gui = gradio.Interface(
        fn = fill_mask, 
        inputs = [
            gradio.components.Textbox(
                lines = 1, 
                label = "Masked Text",
                placeholder = "Enter Text… "),
            gradio.components.Radio(
                label = "Model", 
                choices = MODELS, 
                value = "xlm-roberta-base")
            ], 
        outputs = gradio.Label(label="Suggestions"), 
        allow_flagging = "auto", 
        theme = 'gradio/soft',
        title = "Masked Language Modeling",
        examples = examples)

    # requests will be sent over a websocket instead
    gui.queue(
        # This parameter is used to set the number of worker threads in the Gradio 
        # server that will be processing your requests in parallel
        concurrency_count = 8,
        # Maximum number of requests that the queue processes
        # If a request arrives when the queue is already of the maximum size, 
        # it will not be allowed to join the queue and instead, the user will
        # receive an error saying that the queue is full and to try again
        max_size = 8, 
        # restrict all traffic to happen through the user interface
        # prevents programmatic requests
        api_open = False)

    # launch the gui
    gui.launch(share=args.share)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", help="whether to create a public link for sharing", action="store_true")
    args = parser.parse_args()
    main(args)

