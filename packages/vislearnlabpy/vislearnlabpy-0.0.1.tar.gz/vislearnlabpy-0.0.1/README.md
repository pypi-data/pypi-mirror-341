# vllpy

This is a package with common utility functions, files and pipelines for the Visual Learning Lab. Creating a conda environment is recommended but optional. This package uses python=3.12.

```
conda create -n vislearnlabpy python=3.12
conda activate vislearnlabpy
```

Then, activate the environment and simply install vislearnlabpy via running the following pip command in your terminal. You will also have to install [PyTorch](https://pytorch.org/) and CLIP manually.

```
pip install git+https://github.com/openai/CLIP.git
pip install --upgrade vislearnlabpy
```

To install PyTorch on the Tversky server, run:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
