import logging


portal_logger = logging.getLogger('portal')
task_logger = logging.getLogger('task')


def get_logger(logger_name):
    return logging.getLogger(logger_name)
