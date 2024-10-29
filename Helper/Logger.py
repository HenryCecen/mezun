import logging
import os

class Log():
    def __init__(self, log_file='app.log'):
        log_directory = 'Outputs'
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        log_file = os.path.join(log_directory, 'MyAppLogger.log')
        self.logger = logging.getLogger('MyAppLogger')
        self.logger.setLevel(logging.DEBUG)

        # Create file handler which logs even debug messages
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(fh)

    def info(self, msg):
        self.logger.info(msg)
