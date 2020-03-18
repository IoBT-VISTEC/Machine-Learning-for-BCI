from kivy.app import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from experiment.guide_arrow import GuideArrow
from config.appearance import ARROW_MARGIN, INSTRUCTION_SCREEN_FONT_SIZE


class TextScreen(Widget):
    def __init__(
            self, container, condition_id=None, instruction_text=None,
            arrow_direction=None, arrow_color=None, arrow_size=None, duration=None,
            callback=None, **kwargs
    ):
        super(TextScreen, self).__init__(**kwargs)
        self.container = container
        self.condition_id = condition_id
        self.instruction_text = instruction_text
        self.arrow_direction = arrow_direction
        self.arrow_color = arrow_color
        self.arrow_size = arrow_size
        self.duration = duration
        self.label_condition_id = None
        self.label_instruction_text = None
        self.arrow = None
        self.callback = callback
        self.layout()
        # for adjusting layout after resizing
        self.container.bind(size=self.layout)
        Clock.schedule_once(lambda _: self.finish(), self.duration)

    def layout(self, *_):
        if self.label_condition_id:
            self.container.remove_widget(self.label_condition_id)
        if self.label_instruction_text:
            self.container.remove_widget(self.label_instruction_text)
        if self.arrow:
            self.container.remove_widget(self.arrow)
        if self.condition_id is not None:
            self.label_condition_id = Label(
                font_size=INSTRUCTION_SCREEN_FONT_SIZE,
                text=f"Condition {self.condition_id}",
                size_hint=(0.2, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.52}
            )
        if self.instruction_text is not None:
            self.label_instruction_text = Label(
                font_size=INSTRUCTION_SCREEN_FONT_SIZE,
                text=self.instruction_text,
                size_hint=(0.2, 0.1),
                pos_hint={'center_x': 0.5, 'center_y': 0.47}
            )
        if self.arrow_direction is not None and self.arrow_color is not None and self.arrow_size is not None:
            self.arrow = GuideArrow(ARROW_MARGIN, self.arrow_direction, self.arrow_color, self.arrow_size)
        if self.label_condition_id is not None:
            self.container.add_widget(self.label_condition_id)
        if self.label_instruction_text is not None:
            self.container.add_widget(self.label_instruction_text)
        if self.arrow is not None:
            self.container.add_widget(self.arrow)

    def finish(self):
        if self.label_condition_id is not None:
            self.container.remove_widget(self.label_condition_id)
        if self.label_instruction_text is not None:
            self.container.remove_widget(self.label_instruction_text)
        if self.arrow is not None:
            self.container.remove_widget(self.arrow)
        if self.callback is not None:
            self.callback()
