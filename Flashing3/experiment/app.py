from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from config import experiment_setup, appearance
from experiment.story import Story
import logging

logger = logging.getLogger('FLASHING_EXPERIMENT')
Config.set('graphics', 'maxfps', experiment_setup.MAX_FPS)
logger.info('Set max FPS to', Config.get('graphics', 'maxfps'))
# Config.set('kivy', 'log_level', 'error')
# Config.set("kivy", "log_enable", "0")
if appearance.FULL_SCREEN:
#     Config.set('graphics', 'fullscreen', 'auto')
# print('FULL_SCREEN', appearance.FULL_SCREEN)

    Window.fullscreen = 'auto'

class Main(App):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        self.box = FloatLayout()

    def build(self):
        Story(self.box, experiment_setup.story_setup, self.restart_app)
        return self.box

    def restart_app(self):
        self.box.clear_widgets()
        self.build()


if __name__ == "__main__":
    Main().run()
