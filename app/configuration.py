"""Define 'env vars' and 'log file'
"""

from logging import DEBUG, FileHandler, basicConfig
from os import path

from dotenv import load_dotenv


def logging_configuration(filename):
    basicConfig(
        level=DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[FileHandler(filename, 'a')],
    )


def start_setting_env_vars_and_log_file():
    """Load env vars and define name logging file.

    >>> start_setting_env_vars_and_log_file()
    """
    APP_FOLDER_CONFIGURATION = path.dirname(__file__) + '/'
    APP_NAME = APP_FOLDER_CONFIGURATION.split('/')[-3]

    LOG_FILE_SAME_NAME_OF_APP = APP_FOLDER_CONFIGURATION + APP_NAME + '.log'
    logging_configuration(LOG_FILE_SAME_NAME_OF_APP)

    load_dotenv(APP_FOLDER_CONFIGURATION + '.env')
    load_dotenv(APP_FOLDER_CONFIGURATION + '.env.secrets')
