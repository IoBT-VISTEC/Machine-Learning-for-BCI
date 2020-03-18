from experiment.flickering_tile import FlickeringTile
from kivy.clock import Clock


class Scenario:
    def __init__(self, container, scenario_setup, duration, callback=None):
        self.setup = scenario_setup
        self.total_actor = len(self.setup['tiles'])
        self.current_finish_actor = 0
        self.container = container
        self.duration = duration
        self.statistics = []
        self.callback = callback

    def play(self):
        if len(self.setup['tiles']) == 0:
            return Clock.schedule_once(lambda _: self.finish_one(), self.duration)
        for tile_config in self.setup['tiles']:
            tile = FlickeringTile(
                scene_config=self.setup['scene'],
                tile_config=tile_config,
                duration=self.duration,
                callback=self.finish_one
            )
            self.container.add_widget(tile)

    def finish_one(self, statistic=None):
        self.current_finish_actor += 1
        if statistic is not None and len(statistic) > 0:
            self.statistics.append(statistic)
        if self.current_finish_actor >= self.total_actor:
            self.current_finish_actor = 0
            self.callback(statistics=self.statistics)
