import logging
import datetime
import time

class logger():

    def __init__(self, name = "logger_"):
        self.filename = name + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.csv' # name + datetime
        self.config_log()
        self.t_init = time.monotonic()

    def config_log(self):
        logging.basicConfig(filename = self.filename, encoding='utf-8', level=logging.INFO, format='%(message)s')

    def array2csv(self, arr):
        arr_str = [str(num) for num in arr]
        log_str = ','.join(arr_str)
        return log_str

    def log_data(self, arr):
        log_str = self.array2csv(arr)
        logging.info(log_str)
        pass

    def close_log():
        pass

