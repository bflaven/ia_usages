
"""
# Conda Environment
conda create --name ia_spacy_llm python=3.9.13
conda info --envs
source activate ia_spacy_llm
conda deactivate


export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_API_ORG="your-openai-api-org"



cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_spacy_llm/spacy-llm-examples/usage_examples/ner_v3_openai


"""



from pathlib import Path

import typer
from wasabi import msg

from spacy_llm.util import assemble

Arg = typer.Argument
Opt = typer.Option


def run_pipeline(
    # fmt: off
    text: str = Arg("", help="Text to perform Named Entity Recognition on."),
    config_path: Path = Arg(..., help="Path to the configuration file to use."),
    examples_path: Path = Arg(..., help="Path to the examples file to use."),
    verbose: bool = Opt(False, "--verbose", "-v", help="Show extra information."),
    # fmt: on
):
    msg.text(f"Loading config from {config_path}", show=verbose)
    nlp = assemble(config_path, overrides={"paths.examples": str(examples_path)})
    doc = nlp(text)

    msg.text(f"Text: {doc.text}")
    msg.text(f"Entities: {[(ent.text, ent.label_) for ent in doc.ents]}")


if __name__ == "__main__":
    typer.run(run_pipeline)
