# ia_translation_gradio


**The post is released on my Blog**

Crafting Fluent Translation API: A quick Journey into Text Translation with NLLB, HuggingFace, and FastAPI, Plus a small Dive into Roberta Masked Language Modeling with Gradio. [https://flaven.fr/2023/11/crafting-fluent-translation-api-a-quick-journey-into-text-translation-with-nllb-huggingface-and-fastapi-plus-a-small-dive-into-roberta-masked-language-modeling-with-gradio/](https://flaven.fr/2023/11/crafting-fluent-translation-api-a-quick-journey-into-text-translation-with-nllb-huggingface-and-fastapi-plus-a-small-dive-into-roberta-masked-language-modeling-with-gradio/)


Some use cases for translation with IA and coincidently how to use No Language Left Behind (for instance nllb-200-distilled-600M), transformers, langdetect and Gradio. Also an attempt on gradio and my dear FastAPI!



- No Language Left Behind (for instance nllb-200-distilled-600M) "Driving inclusion through the power of AI translation"
https://ai.meta.com/research/no-language-left-behind/



```bash
001a_giladd123_nllb_fastapi # an attempt using No Language Left Behind (for instance nllb-200-distilled-600M) aka nllb and FastAPI to offer an endpoint for translation
002_mlearning_ai # using langdetect and again nllb
003_using_gradio # using gradio, some concepts + again for translation extracted from https://huggingface.co/spaces/Geonmo/nllb-translation-demo
004_pyyush_maskedlanguagemodeling # a usecase with FastAPI and Roberta (xlm-roberta-base, xlm-roberta-large) for Masked language modeling. 
README.md # this readme
```

**GIT COMMANDS REMINDER**

```bash

# go to the directory
cd /Users/brunoflaven/Documents/03_git/ia_usages/

cd /Users/brunoflaven/Documents/03_git/ia_usages/ia_translation_gradio/004_pyyush_maskedlanguagemodeling

# remove git stuff
ls -la
rm -R .git

# know your branch
git branch


# check for status
git status


# for any change just type this command
git add .

# add a commit with a message
git commit -am "add usecase"
git commit -am "add files"
git commit -am "update files"
git commit -am "add files and update readme"
git commit -am "add to .svg the Musk\'s Favorite Letter X"
git commit -am "add .gitignore"
git commit -am "add docker files"


# push to github if your branch on github is master
# git push origin master
git push

# Repair Permissions
cd /Users/brunoflaven/Documents/03_git/ia_usages
# groupname is staff on a mac
sudo chgrp -R groupname .
sudo chmod -R g+rwX .
sudo find . -type d -exec chmod g+s '{}' +




```
