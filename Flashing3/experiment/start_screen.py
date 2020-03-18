from kivy.app import Widget
from kivy.uix.button import Button


class StartScreen(Widget):
    def __init__(self, container, callback, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        self.container = container
        self.button = None
        self.callback = callback
        self.layout()

    def layout(self):
        self.button = Button(text='start', size_hint=(0.2, 0.1), pos_hint={'center_x': 0.5, 'center_y': .1})
        self.container.add_widget(self.button)
        self.button.bind(on_press=self.finish)

    def finish(self, _):
        self.container.remove_widget(self.button)
        self.callback()
