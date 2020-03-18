import numpy as np
import logging

logger = logging.getLogger('FLASHING_EXPERIMENT')


class Statistic:
    def __init__(self):
        self.stores = {}

    def add_data(self, data):
        frequency = data['frequency']
        data_obj = data['data']
        if frequency not in self.stores:
            self.stores[frequency] = data_obj
        else:
            for key in data_obj.keys():
                if key not in self.stores[frequency]:
                    self.stores[frequency][key] = data_obj[key]
                else:
                    self.stores[frequency][key] += data_obj[key]

    def report(self):
        logging.info('On Exit Report')
        for frequency in self.stores.keys():
            logging.info('Tile with %.2f hz:' % float(frequency))
            logging.info('Average Frequency: %.4f' % (1 / np.mean(self.stores[frequency]['period'])))
            logging.info('Average Absolute Error: %.2f%%' % (np.mean(self.stores[frequency]['error']) * 100))
            logging.info('SD of Frequency: %.2f' % (np.std(self.stores[frequency]['period'])))
            logging.info('Average Absolute FPS: %.2f fps' % np.mean(self.stores[frequency]['fps']))
