from experiment.scenario import Scenario
from experiment.start_screen import StartScreen
from experiment.text_screen import TextScreen
from experiment.statistics import Statistic
import random
import logging
import math
from config.experiment_setup import guide_arrows
from config.appearance import ARROW_SIZE

logger = logging.getLogger('FLASHING_EXPERIMENT')


class ScreenType:
    START_SCREEN = 0
    EXPERIMENT_SCENARIO = 1
    BREAK_TIME = 2
    INSTRUCTION_SCREEN = 3
    BREAK_TIME_INSTRUCTION_SCREEN = 4


class Story:
    def __init__(self, container, story_setup, callback):
        self.container = container
        self.num_episode = story_setup['num_episode']
        self.break_interval = story_setup['break_interval']
        self.scenario_interval = story_setup['scenario_interval']
        self.instruction_interval = story_setup['instruction_interval']
        self.scenarios = story_setup['scenarios']
        self.enable_random = story_setup['enable_random']
        self.enable_start_screen = story_setup['enable_start_screen']
        self.scenario_order = story_setup['scenario_order']
        self.break_scenario = story_setup['break_scenario']
        self.story_line = []
        self.callback = callback
        self.statistics = Statistic()
        self.generate_story_line()
        self.progress_story()

    def generate_random_guiding(self):
        num_round = math.ceil(self.num_episode / len(guide_arrows))
        random_guiding = []
        for scenario in range(len(self.scenarios)):
            scenario_guiding = []
            for _ in range(num_round):
                guiding = guide_arrows.copy()
                random.shuffle(guiding)
                scenario_guiding += guiding
            random_guiding.append(scenario_guiding)
        return random_guiding

    def generate_story_line_sequence(self):
        sequence = []
        for episode in range(self.num_episode):
            if self.enable_random:
                sub_sequence = [i for i in range(len(self.scenarios))]
                random.shuffle(sub_sequence)
            else:
                sub_sequence = self.scenario_order * self.num_episode
                # we will reverse this again at the end
                sub_sequence.reverse()
            sequence.append(sub_sequence)
        return sequence

    def generate_story_line(self):
        # reset story line
        self.story_line = []
        if self.enable_start_screen:
            self.story_line.append({
                'type': ScreenType.START_SCREEN
            })
        episodes = self.generate_story_line_sequence()
        random_guiding = self.generate_random_guiding()
        logger.info(
            f'start a new experiment running each condition for {len(episodes)} ' +
            'times with break time between each scenario'
        )
        for episode in range(len(episodes)):
            guiding_index = 0
            self.story_line.append({
                'type': ScreenType.BREAK_TIME_INSTRUCTION_SCREEN
            })
            self.story_line.append({
                'type': ScreenType.BREAK_TIME
            })
            for index in range(len(episodes[episode])):
                self.story_line.append({
                    'index': index,
                    'arrow_direction': random_guiding[guiding_index][episode],
                    'type': ScreenType.INSTRUCTION_SCREEN,
                    'scenario_id': episodes[episode][index]
                })
                self.story_line.append({
                    'index': index,
                    'arrow_direction': random_guiding[guiding_index][episode],
                    'type': ScreenType.EXPERIMENT_SCENARIO,
                    'scenario_id': episodes[episode][index]
                })
                guiding_index += 1
        # we reverse this to make it easier to be popped in self.progress_story()
        self.story_line = list(reversed(self.story_line))

    def progress_story(self, statistics=()):
        if statistics is not None and len(statistics) > 0:
            for data in statistics:
                self.statistics.add_data(data)

        # we reverse the story line to make it easier to pop
        # the first scenario in our loop
        if len(self.story_line) > 0:
            scene = self.story_line.pop()
            logger.info(f'playing {scene}')
            if scene['type'] == ScreenType.START_SCREEN:
                StartScreen(self.container, self.progress_story)
            elif scene['type'] == ScreenType.INSTRUCTION_SCREEN:
                TextScreen(
                    self.container,
                    self.scenarios[scene['scenario_id']]['condition_id'],
                    self.scenarios[scene['scenario_id']]['instruction_text'],
                    scene['arrow_direction'],
                    self.scenarios[scene['scenario_id']]['guide_arrow_color'],
                    ARROW_SIZE,
                    self.instruction_interval,
                    self.progress_story
                )
            elif scene['type'] == ScreenType.EXPERIMENT_SCENARIO:
                logger.info(f'running a scenario id:{scene["scenario_id"]}')
                Scenario(
                    self.container,
                    self.scenarios[scene['scenario_id']],
                    self.scenario_interval,
                    self.progress_story
                ).play()
            elif scene['type'] == ScreenType.BREAK_TIME_INSTRUCTION_SCREEN:
                logger.info(f'break time instruction screen')
                TextScreen(
                    container=self.container,
                    condition_id=None,
                    instruction_text=f"Rest time for {self.break_interval}s",
                    arrow_direction=None,
                    arrow_color=None,
                    arrow_size=None,
                    duration=self.instruction_interval,
                    callback=self.progress_story
                )
            elif scene['type'] == ScreenType.BREAK_TIME:
                logger.info(f'break time')
                Scenario(
                    self.container,
                    self.break_scenario,
                    self.break_interval,
                    self.progress_story
                ).play()
        else:
            logger.info(f'finish experiment')
            self.finish()

    def report_statistic(self):
        self.statistics.report()

    def finish(self):
        self.report_statistic()
        self.callback()
