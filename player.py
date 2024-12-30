import math
from typing import Optional
from typing import Union

from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

from attack import EllipseAttack
from attack import LineAttack
from item import Item
from item import LootType
from textures import textures


class Player(Widget):
    keys = set()
    direction = Vector(0, 0)
    velocity_multiplier = NumericProperty(200)
    health = NumericProperty(100)

    attack_position = Vector(None, None)
    attack_time = 0
    pickup_distance = 25
    inventory: dict[str, Optional[Item]] = {
        "1": Item(loot_type=LootType["ATTACK_ELLIPSE"]),
        "2": None,
        "3": None,
        "4": None,
        "5": None,
        "6": None,
        "7": None,
        "8": None,
        "9": None,
        "0": None,
    }
    flip_texture = False

    @property
    def center_pos(self):
        return Vector(*self.pos) + (51 / 2, 38 / 2)

    def reset(self):
        self.health = 100
        self.attack_time = 0
        self.inventory = {
            "1": Item(loot_type=LootType["ATTACK_ELLIPSE"]),
            "2": None,
            "3": None,
            "4": None,
            "5": None,
            "6": None,
            "7": None,
            "8": None,
            "9": None,
            "0": None,
        }

    def update(self, dt, tick):
        self.direction.x = -1 if "a" in self.keys else 1 if "d" in self.keys else 0
        self.direction.y = 1 if "w" in self.keys else -1 if "s" in self.keys else 0
        self.pos = self.direction.normalize() * self.velocity_multiplier * dt + self.pos

        with self.canvas:
            self.canvas.clear()
            Color(1, 1, 1, 1 - (100 - self.health) / 100)
            self.flip_texture = (
                True
                if self.direction.x < 0
                else False
                if self.direction.x > 0
                else self.flip_texture
            )
            texture = textures["minawan.png" if self.flip_texture else "flip_minawan.png"]
            Rectangle(
                texture=texture,
                pos=self.pos,
                size=(51, 38),
            )

        if self.attack_time < tick + 10 and self.attack_position.x and self.attack_position.y:
            self.attack_time = tick
            x1, y1 = self.attack_position
            x2, y2 = self.center_pos
            angle = math.degrees(math.atan2(y1 - y2, x1 - x2))
            if Vector(x1, y1).distance((x2, y2)) > 150:
                x1 = x2 + 150 * math.cos(math.radians(angle))
                y1 = y2 + 150 * math.sin(math.radians(angle))

            attacks_info = list()
            attack_graphics = list()

            for item in self.inventory.values():
                if item is None:
                    continue
                if item.loot_type in (LineAttack, EllipseAttack):
                    attacks_info.append([item])
                elif attacks_info:
                    attacks_info[-1].append(item)

            for attack_info in attacks_info:
                attack: Union[EllipseAttack, LineAttack] = attack_info[0].loot_type
                args = dict(
                    x1=x1,
                    y1=y1,
                    length=0.8,
                    size=10,
                    damage=10,
                    direction=math.degrees(math.atan2(y1 - y2, x1 - x2)),
                )
                for modifier in attack_info[1:]:
                    args = modifier.loot_type(**args)
                attack_graphics.append(attack(**args))

                x1 = args["x1"] + args["size"] * 5 * math.cos(math.radians(args["direction"]))
                y1 = args["y1"] + args["size"] * 5 * math.sin(math.radians(args["direction"]))

            return attack_graphics
        return None
