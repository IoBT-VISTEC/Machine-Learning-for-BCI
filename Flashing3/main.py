from experiment.app import Main
import logging

# setup our own log
logger = logging.getLogger('FLASHING_EXPERIMENT', )
console_handler = logging.StreamHandler()
c_format = logging.Formatter('[%(name)s:%(levelname)s] %(message)s')
console_handler.setFormatter(c_format)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__":
    Main().run()
