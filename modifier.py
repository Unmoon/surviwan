import random


def size_mod(**kwargs):
    kwargs["size"] = kwargs["size"] * 2
    return kwargs


def damage_mod(**kwargs):
    kwargs["damage"] = kwargs["damage"] * 2
    return kwargs


def speed_mod(**kwargs):
    kwargs["length"] = kwargs["length"] / 2
    return kwargs


def direction_mod(**kwargs):
    kwargs["direction"] = random.uniform(-180, 180)
    return kwargs
