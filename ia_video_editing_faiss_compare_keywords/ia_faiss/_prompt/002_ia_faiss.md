
# 002_ia_faiss.md

## PROMPT_1
As python expert can you detail the install of Faiss with the help of conda,  give step by step all the required commands.

## PERPLEXITY_1

To install Faiss using Conda, follow these step-by-step instructions:

1. Install Miniconda (if not already installed):
   - Download the Miniconda installer from the official website
   - Open a terminal and run the installer:
     ```bash
     bash Miniconda3-latest-Linux-x86_64.sh
     ```
   - Follow the prompts to complete the installation

2. Create a new Conda environment:
   ```bash
   conda create --name faiss_env python=3.9
   ```

3. Activate the new environment:
   ```bash
   conda activate faiss_env
   ```

4. Install Faiss:
   - For CPU-only version:
     ```bash
     conda install -c pytorch faiss-cpu
     ```
   - For GPU version (CUDA 11.4 or 12.1):
     ```bash
     conda install -c pytorch -c nvidia faiss-gpu
     ```

5. Verify the installation:
   ```python
   import faiss
   print(faiss.__version__)
   ```

If you need a specific combination of Faiss, CUDA, and PyTorch, you can use the following command[1]:

```bash
conda install -c pytorch -c nvidia faiss-gpu=1.8.0 pytorch=*=*cuda* pytorch-cuda=11 numpy
```

This command installs Faiss 1.8.0 with CUDA support and compatible versions of PyTorch and NumPy[1].

Remember to activate your Conda environment (`conda activate faiss_env`) every time you want to use Faiss in a new terminal session.

Citations:
[1] https://github.com/facebookresearch/faiss/blob/main/INSTALL.md
[2] https://cheatsheet.md/vector-database/faiss-python-api
[3] https://stackoverflow.com/questions/58957169/faiss-error-could-not-find-a-version-that-satisfies-the-requirement-faiss-from/71968177
[4] https://github.com/shiwendai/Faiss/blob/master/INSTALL.md
[5] https://github.com/facebookresearch/faiss/wiki/Installing-Faiss
[6] https://myscale.com/blog/faiss-install-pip-quick-guide/
[7] https://www.reddit.com/r/LangChain/comments/16tnhyi/best_recommended_way_to_install_faiss/
[8] https://www.kaggle.com/code/francescosabbarese97/python-expert-rag-using-gemma-langchain-and-faiss/notebook
[9] https://www.restack.io/p/faiss-gpu-answer-installing-windows-cat-ai