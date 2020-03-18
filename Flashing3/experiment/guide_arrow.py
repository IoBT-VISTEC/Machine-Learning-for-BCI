from kivy.app import Widget
from kivy.graphics.vertex_instructions import (Line, Triangle)
from kivy.graphics.context_instructions import Color
from kivy.core.window import Window
from config import appearance


class GuideArrow(Widget):
    def __init__(self, margin, direction, arrow_color, arrow_length, **kwargs):
        super(GuideArrow, self).__init__(**kwargs)
        self.direction = direction
        self.arrow_length = arrow_length
        self.arrow_tip_size = 0.02
        self.arrow_color = arrow_color
        self.margin = margin
        self.draw()

    def calculate_arrow_origin(self):
        width, height = Window.width, Window.height
        if self.direction == 'TOP':
            return 0.5 * width, (1 - self.margin) * height
        if self.direction == 'BOTTOM':
            return 0.5 * width, self.margin * height
        if self.direction == 'LEFT':
            return self.margin * width, 0.5 * height
        if self.direction == 'RIGHT':
            return (1 - self.margin) * width, 0.5 * height

    def calculate_arrow_tip_position(self):
        x, y = self.calculate_arrow_origin()
        width, height = Window.width, Window.height
        size = min(width, height)
        if self.direction == 'TOP':
            return x, y + size * self.arrow_length
        if self.direction == 'BOTTOM':
            return x, y - size * self.arrow_length
        if self.direction == 'LEFT':
            return x - size * self.arrow_length, y
        if self.direction == 'RIGHT':
            return x + size * self.arrow_length, y

    def generate_arrow_tip_position(self):
        tip_pos = self.calculate_arrow_tip_position()
        width, height = Window.width, Window.height
        size = min(width, height)
        offset = self.arrow_tip_size * size
        half_offset = offset / 2
        if self.direction == 'TOP':
            # tip_pos = (x_mid, y_mid * (1 + self.arrow_length))
            triangle = (
                tip_pos[0], tip_pos[1] + offset,
                tip_pos[0] + half_offset, tip_pos[1],
                tip_pos[0] - half_offset, tip_pos[1],
            )
            return triangle
        if self.direction == 'BOTTOM':
            # tip_pos = (x_mid, y_mid * (1 - self.arrow_length))
            triangle = (
                tip_pos[0], tip_pos[1] - offset,
                tip_pos[0] + half_offset, tip_pos[1],
                tip_pos[0] - half_offset, tip_pos[1],
            )
            return triangle
        if self.direction == 'RIGHT':
            # tip_pos = (x_mid * (1 + self.arrow_length), y_mid)
            triangle = (
                tip_pos[0] + offset, tip_pos[1],
                tip_pos[0], tip_pos[1] + half_offset,
                tip_pos[0], tip_pos[1] - half_offset
            )
            return triangle
        if self.direction == 'LEFT':
            # tip_pos = (x_mid * (1 - self.arrow_length), y_mid)
            triangle = (
                tip_pos[0] - offset, tip_pos[1],
                tip_pos[0], tip_pos[1] + half_offset,
                tip_pos[0], tip_pos[1] - half_offset
            )
            return triangle

    def get_pos(self):
        line = self.calculate_arrow_origin() + self.calculate_arrow_tip_position()
        triangle = self.generate_arrow_tip_position()
        return line, triangle

    def draw(self):
        if self.arrow_color is None:
            return None
        line, triangle = self.get_pos()
        with self.canvas:
            self.canvas.clear()
            Color(*appearance.COLOR[self.arrow_color])
            Line(points=line, width=2)
            Triangle(points=triangle)

    def finish(self):
        with self.canvas:
            self.canvas.clear()
