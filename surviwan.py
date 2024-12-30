import random
from typing import Union

from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from attack import EllipseAttack
from attack import LineAttack
from enemy import Enemy
from inventory import Inventory
from inventory import InventoryText
from item import Item
from item import LootType
from player import Player
from textures import load_textures

GLOBAL_COOLDOWN = 0.01  # seconds


class SurviwanGame(Widget):
    player: Player = ObjectProperty(None)
    enemies: set[Enemy] = set()
    attacks: set[Union[EllipseAttack, LineAttack]] = set()
    last_attack: float = 0
    last_spawn: float = 0
    score: int = 0
    loot: set[Item] = set()
    inventory: Inventory = Inventory()
    inventory_text = InventoryText()
    score_text = Label(text="")

    def __init__(self, **kwargs):
        super(SurviwanGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self, "text")
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def reset(self):
        self.enemies.clear()
        self.attacks.clear()
        self.last_attack = 0
        self.last_spawn = 0
        self.score = 0
        self.loot.clear()
        self.player.pos = self.center
        self.player.reset()
        Clock.schedule_interval(self.update, 1.0 / 120.0)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        if key in ("w", "s", "a", "d", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
            self.player.keys.add(key)
            return True
        return False

    def _on_keyboard_up(self, keyboard, keycode):
        key = keycode[1]
        if key in ("w", "s", "a", "d", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
            self.player.keys.discard(key)
            return True
        if self.player.health == 0 and key in ("spacebar", "enter", "r"):
            self.reset()
            return True
        return False

    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=self.pos, size=self.size)

            if self.player.health <= 0:
                Clock.unschedule(self.update)
                self.score_text.text = (
                    f"Ghosts sent you packing after just you helped just {self.score} of them!"
                )
            elif self.score > 1111:
                self.score_text.text = f"{self.score} ghosts sent back home, wanwan!"
            else:
                self.score_text.text = f"{self.score} ghosts sent back home"
            self.score_text.center = self.center_x, self.height - 25
            self.canvas.add(self.score_text.canvas)

            self.inventory.center_x = self.center_x
            self.canvas.add(self.inventory.update(self.player.inventory))

            self.inventory_text.center = self.center_x - 25, 50
            self.canvas.add(self.inventory_text.canvas)

            tick = Clock.get_time()

            if self.last_spawn + (0.5 - self.score / 1000) < tick:
                self.last_spawn = tick
                if random.choice((True, False)):
                    x = random.choice((0, self.size[0]))
                    y = random.randint(0, self.size[1])
                else:
                    x = random.randint(0, self.size[0])
                    y = random.choice((0, self.size[1]))
                self.enemies.add(Enemy(pos=(x, y), velocity_multiplier=40 + self.score / 10))

            attacks = self.player.update(dt, tick)
            if attacks is not None and self.last_attack + GLOBAL_COOLDOWN < tick:
                self.attacks.update(set(attacks))
                self.last_attack = tick

            to_remove = []

            for enemy in self.enemies:
                graphic = enemy.update(dt, tick, player_pos=self.player.center_pos)
                if not graphic:
                    to_remove.append(enemy)
                    self.score += 1
                    if random.random() > 0.9:
                        self.loot.add(
                            Item(
                                pos=(*enemy.center_pos,),
                                loot_type=random.choice(list(LootType.values())),
                                created=tick,
                            )
                        )
                else:
                    self.canvas.add(graphic)
                    if enemy.check_hit(self.player.center_pos, tick):
                        self.player.health -= enemy.attack_damage

            for loot in self.loot:
                graphic = loot.update(dt, tick)
                if graphic is None:
                    to_remove.append(loot)
                    continue
                self.canvas.add(graphic)
                if loot.can_pickup(self.player.center_pos, self.player.pickup_distance):
                    if loot.loot_type is None:
                        self.player.health = 100
                        to_remove.append(loot)
                        continue
                    keys = list(
                        self.player.keys.intersection(
                            {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0"}
                        )
                    )
                    if keys:
                        self.player.inventory[keys[0]] = loot
                        to_remove.append(loot)

            for attack in self.attacks:
                graphic = attack.update(dt, tick)
                if not graphic:
                    to_remove.append(attack)
                else:
                    self.canvas.add(graphic)
                    for enemy in self.enemies:
                        if attack.check_hit(enemy.center_pos, enemy.render_size):
                            enemy.health -= attack.damage
                    attack.hit_checked = True

            self.attacks.difference_update(to_remove)
            self.enemies.difference_update(to_remove)
            self.loot.difference_update(to_remove)

            self.canvas.add(self.player.canvas)

    def on_touch_down(self, touch):
        self.player.attack_position.x = touch.x
        self.player.attack_position.y = touch.y

    def on_touch_move(self, touch):
        self.player.attack_position.x = touch.x
        self.player.attack_position.y = touch.y

    def on_touch_up(self, touch):
        self.player.attack_position.x = None
        self.player.attack_position.y = None


class SurviwanApp(App):
    def build(self):
        load_textures()
        Window.maximize()
        game = SurviwanGame()
        Clock.schedule_interval(game.update, 1.0 / 120.0)
        return game


if __name__ == "__main__":
    Config.set("input", "mouse", "mouse,disable_multitouch")
    SurviwanApp().run()
