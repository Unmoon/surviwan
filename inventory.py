from typing import Optional

from kivy.graphics import Color
from kivy.graphics import Ellipse
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from item import Item


class InventoryText(BoxLayout):
    orientation = "horizontal"

    def __init__(self, **kwargs):
        super().__init__(size=(500, 50), **kwargs)
        self.add_widget(Label(text="1"))
        self.add_widget(Label(text="2"))
        self.add_widget(Label(text="3"))
        self.add_widget(Label(text="4"))
        self.add_widget(Label(text="5"))
        self.add_widget(Label(text="6"))
        self.add_widget(Label(text="7"))
        self.add_widget(Label(text="8"))
        self.add_widget(Label(text="9"))
        self.add_widget(Label(text="0"))


class Inventory(Widget):
    def __init__(self, **kwargs):
        super().__init__(size=(500, 50), **kwargs)

    def update(self, items: dict[str, Optional[Item]]):
        with self.canvas:
            self.canvas.clear()

            for index, item in enumerate(items.values()):
                if item is None:
                    continue
                item.pos = (self.center_x - 258 + index * 50, 0)
                self.canvas.add(item.update(0, 0, solid=True))
        return self.canvas
