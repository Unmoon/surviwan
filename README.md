# Surviwan
## For Neuro-sama Game Jam 2
https://unmoon.itch.io/surviwan

### Running from source

You will need to add the following textures to textures folder. See itch.io page for source of textures used in release. They can't be included in git due to licensing.

 - big.png
 - flip_ghost.png
 - flip_ghost_red.png
 - ghost.png
 - ghost_red.png
 - hammer.png
 - heart.png
 - line.png
 - rng.png
 - sphere.png

`python -m pip install -U pip setuptools`  
`python -m pip install kivy[base]`  
`python surviwan.py`

### Building executable

`python -m pip install pyinstaller`  
`python -m PyInstaller surviwan.spec`