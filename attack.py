import math

from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Ellipse
from kivy.graphics import Line
from kivy.uix.widget import Widget
from kivy.vector import Vector


class EllipseAttack(Widget):
    def __init__(self, x1, y1, length, size, damage, direction, **kwargs):
        super().__init__(**kwargs)
        self.length = length
        self.start = Clock.get_time()
        self.original_attack_size = size
        self.attack_size = self.original_attack_size
        self.damage = damage
        self.angle = direction
        self.hit_checked = False
        self.pos = Vector(
            x1 + size * math.cos(math.radians(self.angle)),
            y1 + size * math.sin(math.radians(self.angle)),
        )

    def update(self, dt, tick):
        if tick == self.start:
            left = 1
        else:
            left = 1 - (tick - self.start) / self.length
        if left < 0:
            return False
        self.attack_size = self.original_attack_size * left
        with self.canvas:
            self.canvas.clear()
            Color(0.8, 0.3, 0.0, 0.5)
            Ellipse(
                pos=Vector(self.pos) - (self.attack_size / 2, self.attack_size / 2),
                size=(self.attack_size, self.attack_size),
            )
        return self.canvas

    def check_hit(self, pos: Vector, enemy_size: float):
        if self.hit_checked:
            return False
        return Vector(*self.pos).distance(Vector(*pos)) < self.attack_size + enemy_size / 2


class LineAttack(Widget):
    def __init__(self, x1, y1, length, size, damage, direction, **kwargs):
        super().__init__(**kwargs)
        self.start_pos = Vector(x1, y1)
        self.start = Clock.get_time()
        self.length = length
        self.original_attack_size = size / 2
        self.attack_size = self.original_attack_size
        self.damage = damage
        self.angle = direction
        self.hit_checked = False
        self.line_length = size * 5
        self.end_pos = Vector(
            self.start_pos.x + self.line_length * math.cos(math.radians(self.angle)),
            self.start_pos.y + self.line_length * math.sin(math.radians(self.angle)),
        )

    def update(self, dt, tick):
        if tick == self.start:
            left = 1
        else:
            left = 1 - (tick - self.start) / self.length
        if left < 0:
            return False
        self.attack_size = self.original_attack_size * left
        with self.canvas:
            self.canvas.clear()
            Color(0.8, 0.3, 0.0, 0.5)
            Line(points=[*self.start_pos, *self.end_pos], width=self.attack_size, cap="round")
        return self.canvas

    def check_hit(self, pos: Vector, enemy_size: float):
        if self.hit_checked:
            return False
        check_size = self.attack_size + enemy_size / 2
        v1 = Vector(
            pos.x + check_size * math.cos(math.radians(self.angle + 90)),
            pos.y + check_size * math.sin(math.radians(self.angle + 90)),
        )
        v2 = Vector(
            pos.x - check_size * math.cos(math.radians(self.angle + 90)),
            pos.y - check_size * math.sin(math.radians(self.angle + 90)),
        )
        return Vector.segment_intersection(v1, v2, self.start_pos, self.end_pos) is not None
