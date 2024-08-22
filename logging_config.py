import logging
import time

date_time = time.time()
output_filename = str('vani_assistant_log' + str(date_time) + '.log')


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Adjust as needed

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add handlers as needed
    file_handler = logging.FileHandler(output_filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

