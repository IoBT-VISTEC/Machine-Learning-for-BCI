from kivy.app import Widget
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics.vertex_instructions import (Rectangle)
from kivy.graphics.context_instructions import Color
import random

from config import appearance, experiment_setup
import math


class FlickeringTile(Widget):
    def __init__(self, tile_config, scene_config, duration, callback, **kwargs):
        super(FlickeringTile, self).__init__(**kwargs)
        self.state = True
        # x, y start from bottom left
        self.rect_x = tile_config['x']
        self.rect_y = tile_config['y']
        self.rect_width = tile_config.get('width')
        self.rect_height = tile_config.get('height')
        self.rect_relative_size = tile_config.get('size', 0.15)
        # 1 frequency has 2 flips (eg. black -> white -> black is called 1 time)
        self.rect_flip_freq = tile_config['frequency'] * 2
        self.frequency = tile_config['frequency']
        self.padding = tile_config.get('pad', 30)
        self.words = scene_config['word_list']
        self.is_word_random = scene_config.get('is_word_random', False)
        self.word_index = 0
        self.callback = callback
        self.rect_event = Clock.schedule_interval(
            lambda time_passed: self.flick(time_passed), 1 / (self.rect_flip_freq + experiment_setup.calibrate_time)
        )
        self.change_text_event = Clock.schedule_interval(
            lambda time_passed: self.change_text(), 1
        )
        self.finish_flickering = Clock.schedule_once(
            self.finish, duration
        )
        self.canvas.clear()

        # Use for further analysis on statistic of diff and fps
        self.statistic = {
            'frequency': self.frequency,
            'data': {
                'period': [],
                'error': [],
                'fps': []
            }
        }
        if appearance.SHOW_TILE_FREQUENCY_LABEL:
            self.label_frequency = Label(text=str(self.frequency) + ' frequency', font_size=30)
        self.label_1 = Label(text='')
        self.label_2 = Label(text='')
        # to init text on each label
        self.change_text()

    # try to make the tiles look most pretty by calculate to position of it
    # base on screen size and tile size
    def get_pos(self):
        width, height = self.get_size()
        if self.rect_x == 'middle' and self.rect_y == 'top':
            return self.width/2 - width/2, self.height - height - self.padding
        if self.rect_x == 'left' and self.rect_y == 'middle':
            return 0 + self.padding, self.height/2 - height/2
        if self.rect_x == 'right' and self.rect_y == 'middle':
            return self.width - width - self.padding, self.height/2 - height/2
        if self.rect_x == 'middle' and self.rect_y == 'bottom':
            return self.width/2 - width/2, 0 + self.padding
        if self.rect_x and self.rect_y:
            return self.rect_x, self.rect_y

    def get_label_pos(self, text_size):
        x, y = self.get_pos()
        width, height = self.get_size()
        text_width, text_height = text_size
        return (x + width / 2 - text_width / 2), (y + height / 2 - text_height / 2)

    def get_size(self):
        if self.rect_width and self.rect_height:
            return self.rect_width, self.rect_height
        return self.width * self.rect_relative_size, self.width * self.rect_relative_size

    def change_text(self):
        # self.label_1.text = self.label_2.text = str(random.randint(0, 100))
        if self.words is None:
            return None
        if self.is_word_random:
            self.label_1.text = self.label_2.text = random.choice(self.words)
        else:
            self.label_1.text = self.label_2.text = self.words[self.word_index]
            self.word_index += 1
            if self.word_index > len(self.words):
                self.word_index = 0

    def flick(self, time_passed):
        self.statistic['data']['period'].append(time_passed * 2)
        self.statistic['data']['error'].append(math.fabs((1 / time_passed - self.rect_flip_freq) / self.rect_flip_freq))
        fps = Clock.get_rfps()
        # Ignore FPS of a few first frames which are 0
        # (fps of Kivy needs some initial frame before reporting the value for us)
        if fps > 0:
            self.statistic['data']['fps'].append(fps)
        size = self.get_size()
        pos = self.get_pos()
        with self.canvas:
            self.canvas.clear()
            if self.state:
                Color(*appearance.COLOR['WHITE'])
            else:
                Color(*appearance.COLOR['BLACK'])
            Rectangle(pos=pos, size=size)

            if self.state:
                self.remove_widget(self.label_2)
                self.label_1.pos = self.get_label_pos(self.label_1.texture_size)
                self.label_1.font_size = size[1] * appearance.TILE_FONT_SIZE_RATIO
                self.label_1.size = self.label_1.texture_size
                self.label_1.color = appearance.LABEL_COLOR['BLACK']
                self.add_widget(self.label_1)
            else:
                self.remove_widget(self.label_1)
                self.label_2.pos = self.get_label_pos(self.label_2.texture_size)
                self.label_2.font_size = size[1] * appearance.TILE_FONT_SIZE_RATIO
                self.label_2.size = self.label_2.texture_size
                self.label_2.color = appearance.LABEL_COLOR['WHITE']
                self.add_widget(self.label_2)

            if appearance.SHOW_TILE_FREQUENCY_LABEL:
                self.remove_widget(self.label_frequency)
                self.label_frequency.pos = pos
                self.add_widget(
                    self.label_frequency
                )
            self.state = not self.state

    def finish(self, _):
        with self.canvas:
            self.canvas.clear()
        self.rect_event.cancel()
        self.change_text_event.cancel()
        self.callback(statistic=self.statistic)
