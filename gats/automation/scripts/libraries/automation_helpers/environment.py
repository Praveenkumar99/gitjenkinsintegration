"""
@Description :
@Author :
@Created on :

"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Environment:
    main_directory_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    TEMP_FOLDER_PATH = os.path.join(main_directory_path, "temp")
    CONFIG_FOLDER_PATH = os.path.join(main_directory_path, "config")
    UI_PARSER_PATH = os.path.join(CONFIG_FOLDER_PATH, "uiconfig.ini")
