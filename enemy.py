from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector

from textures import textures


class Enemy(Widget):
    velocity_multiplier = NumericProperty(40)
    last_attack = NumericProperty(0)
    health = NumericProperty(100)
    attack_damage = 10
    hit = False
    render_size = 32

    @property
    def center_pos(self) -> Vector:
        return Vector(*Vector(*self.pos) + (self.render_size / 2, self.render_size / 2))

    def update(self, dt, tick, player_pos: Vector):
        if self.health < 0:
            return None

        flip = "flip_" if player_pos.x > self.center_pos.x else ""

        difference: Vector = Vector(*self.pos) - player_pos

        if self.last_attack + 1 < tick and difference.length() < 50:
            self.last_attack = tick
            self.hit = False

        texture = textures[flip + "ghost.png"]
        if self.last_attack + 0.5 > tick:
            texture = textures[flip + "ghost_red.png"]
        elif difference.length() > 50:
            normal = difference.normalize() * dt * self.velocity_multiplier
            self.pos = Vector(*self.pos) - normal

        with self.canvas:
            self.canvas.clear()
            Color((0.0, 0.0, 0.0, 1.0))
            Rectangle(
                texture=texture,
                pos=self.pos,
                size=(self.render_size, self.render_size),
            )
        return self.canvas

    def check_hit(self, player_pos: Vector, tick):
        difference: Vector = self.center_pos - player_pos
        if self.last_attack + 0.5 < tick and difference.length() < 50 and not self.hit:
            self.hit = True
            return True
        return False
