from config.random_words import words


calibrate_time = 0
scenarios = [{
    "enable_guide_arrow": True,
    "guide_arrow_color": "RED",
    "condition_id": 3,
    "instruction_text": 'Focus on "word"',
    "scene": {
        "word_list": words,
        "is_word_random": False,
        "word_change_frequency": 1,
    },
    "tiles": [
        {'x': 'middle', 'y': 'top', 'frequency': 6},
        {'x': 'left', 'y': 'middle', 'frequency': 6.57},
        {'x': 'right', 'y': 'middle', 'frequency': 7.5},
        {'x': 'middle', 'y': 'bottom', 'frequency': 8.57}
    ]
}, {
    "enable_guide_arrow": True,
    "guide_arrow_color": "BLUE",
    "condition_id": 2,
    "instruction_text": 'Focus on "square"',
    "scene": {
        "word_list": None,
    },
    "tiles": [
        {'x': 'middle', 'y': 'top', 'frequency': 6},
        {'x': 'left', 'y': 'middle', 'frequency': 6.57},
        {'x': 'right', 'y': 'middle', 'frequency': 7.5},
        {'x': 'middle', 'y': 'bottom', 'frequency': 8.57}
    ]
}, {
    "enable_guide_arrow": True,
    "guide_arrow_color": "GREEN",
    "condition_id": 1,
    "instruction_text": 'Focus on "square"',
    "scene": {
        "word_list": words,
        "is_word_random": False
    },
    "tiles": [
        {'x': 'middle', 'y': 'top', 'frequency': 6},
        {'x': 'left', 'y': 'middle', 'frequency': 6.57},
        {'x': 'right', 'y': 'middle', 'frequency': 7.5},
        {'x': 'middle', 'y': 'bottom', 'frequency': 8.57}
    ]
}]

break_scenario = {
    "word_list": None,
    "tiles": []
}

story_setup = {
    "num_episode": 12,
    "enable_start_screen": True,
    "enable_random": True,
    "scenario_order": [],
    # in second
    "break_interval": 20,
    # in second
    "instruction_interval": 5,
    # in second
    "scenario_interval": 10,
    "scenarios": scenarios,
    "break_scenario": break_scenario
}

guide_arrows = ['TOP', 'BOTTOM', 'LEFT', 'RIGHT']

# maximum frame per second for Kivy this will affect how often
# Clock.schedule_interval check if it needs to run its callback
MAX_FPS = 200
