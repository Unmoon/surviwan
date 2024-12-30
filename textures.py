import sys

from kivy.core.image import Image

textures = {}


def load_textures():
    parent = getattr(sys, "_MEIPASS") + "/" if hasattr(sys, "_MEIPASS") else ""
    for name in (
        "big.png",
        "ghost.png",
        "ghost_red.png",
        "flip_ghost.png",
        "flip_ghost_red.png",
        "flip_minawan.png",
        "hammer.png",
        "heart.png",
        "line.png",
        "minawan.png",
        "rng.png",
        "sphere.png",
    ):
        textures[name] = Image(parent + "textures/" + name).texture
