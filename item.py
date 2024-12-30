from kivy.graphics import Color
from kivy.graphics import Ellipse
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.vector import Vector

from attack import EllipseAttack
from attack import LineAttack
from modifier import *
from textures import textures

LootType = dict(
    HEALTH=None,
    ATTACK_ELLIPSE=EllipseAttack,
    ATTACK_LINE=LineAttack,
    MODIFIER_SIZE=size_mod,
    MODIFIER_DAMAGE=damage_mod,
    MODIFIER_RANDOM_DIRECTION=direction_mod,
)

LootTexture = {
    None: "heart.png",
    EllipseAttack: "sphere.png",
    LineAttack: "line.png",
    size_mod: "big.png",
    damage_mod: "hammer.png",
    direction_mod: "rng.png",
}


class Item(Widget):
    graphic_size = 64

    def __init__(self, loot_type: LootType, created=0, **kwargs):
        super().__init__(**kwargs)
        self.created = created
        self.loot_type = loot_type

    def update(self, dt, tick, solid=False):
        if self.created + 15 < tick and not solid:
            return None
        alpha = abs(1 - tick % 2) if not solid else 1
        with self.canvas:
            self.canvas.clear()
            if solid:
                Color(0, 0, 0)
                Rectangle(pos=self.pos, size=(self.graphic_size, self.graphic_size))
            Color(1, 1, 1, alpha)
            texture = textures[LootTexture.get(self.loot_type)]
            Rectangle(
                texture=texture,
                pos=self.pos,
                size=(self.graphic_size, self.graphic_size),
            )
        return self.canvas

    def can_pickup(self, player_pos: Vector, player_size):
        return player_pos.distance(self.pos) < self.graphic_size + player_size / 2
