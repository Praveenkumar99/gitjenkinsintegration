"""

"""

import logging
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import automation_helpers.logs as log_instance
import automation_helpers.globalconstants as gc


root_log = logging.root
log = logging.getLogger(__name__)

# ---------------------------------------------------
# Setup logging
# ---------------------------------------------------
global file_path


def script_logger_handler(log_directory, filename, level=logging.DEBUG):
    """
    Creates the log handler along with log level and required format
    :param log_directory : contains the name of the log directory
    :param filename : contains the name of the file
    :param level : log level to be set
    :Author : Halli Vinay
    """
    log_directory = os.path.abspath(log_directory)
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    filename = os.path.join(log_directory, filename)
    tc_logger_file_handler = logging.FileHandler(filename)
    tc_logger_file_handler.setLevel(level)
    tc_logger_file_handler.setFormatter(log_instance.FileFormat())
    return tc_logger_file_handler


def setup_logging(file_name, project=None, session=None,
                  device=None, suite=None, iter_count=None):
    """
    Function which contains multiple API calls for creating log directory,
    creating handler, setting the log level and assigning to root log
    :param project: Project name
    :param milestone: Milestone name
    :param session: Session name
    :param device: Thin Client name where it needs to be run
    :param suite: Name of the test suite to be run
    :param file_name: test case name with which the log needs to be created
    :return: Root handler
    :Author         : Halli Vinay
    """
    log.info("executing setup logging")
    log.info("Filename:{0}".format(file_name))
    if project:
        print(f'Inside log_utils_setup:{project}, {suite}, {device}, {session}, {file_name}, {iter_count}')
        logdirectory = _make_log_dir(project, session, device, suite, file_name, iter_count)
    else:
        logdirectory = os.getcwd()

    # assigned for accessing the folder path globally
    gc.IMAGE_FOLDER = logdirectory
    fmt = log_instance.StdFormatter()
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(fmt)
    root_log.addHandler(stdout_handler)
    root_log.setLevel(logging.DEBUG)
    f_name = file_name + "_" + time.strftime('%Y%m%d-%H%M%S')
    script_logger = script_logger_handler(logdirectory, f_name)
    # Filtering logs coming from PIL, Paramiko
    logging.getLogger("PIL.PngImagePlugin").setLevel(logging.CRITICAL + 1)
    logging.getLogger("paramiko").setLevel(logging.CRITICAL + 1)
    logging.getLogger("vncdotool.client").setLevel(logging.CRITICAL + 1)
    logging.getLogger("twisted").setLevel(logging.CRITICAL + 1)
    script_logger.setLevel(logging.DEBUG)
    root_log.addHandler(script_logger)
    log.info('Logging has been setup')
    return root_log


def is_windows():
    """
    :Function Name : is_windows
    escription : to check whether you are running a windows operating system
    :returns : whether you are running a crappy operating system
    :rtype : bool
    :Author         : Halli Vinay
    """
    return sys.platform.startswith('win')


def get_session(session_name):
    """
    method for retrieving logs directory path
    :param session_name: Name of the session
    :return: Log directory path
    :Author         : Halli Vinay
    """
    main_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    log_path = os.path.join(main_dir, "results")
    return os.path.join(log_path, session_name)


def _make_log_dir(project, session, device, suite, file_name, iteration):
    """
    Returns complete log directory path where the logs have to be  stored
    :param project: Project name
    :param session: Session name
    :param device: Thin Client name where it needs to be run
    :param suite: Name of the test suite to be run
    :param file_name: test case name with which the log needs to be created
    :return: Complete log directory path for storing script logs, result images,
    system logs which will be created under test case name
    :Author : Halli Vinay
    """

    print("device:{}".format(device))
    print("suite:{}".format(suite))
    print("file_name:{}".format(file_name))
    print("iteration:{}".format(iteration))

    main_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    log_path = os.path.join(main_dir, "results")
    log_directory = os.path.join(log_path, project, suite,  device, session,
                                 file_name, iteration)
    print("log_directory:{}".format(log_directory))
    gc.ROBOT_LOG_PATH = log_directory

    return log_directory


def image_and_yaml_copy_dir(project, session, device):
    session_dir = os.path.join(project, "test_configuration", session)
    log_directory = os.path.join(get_session(session_dir), device)
    gc.LOG_FILE_PATH = log_directory

    logdirectory = os.path.abspath(log_directory)
    if not os.path.exists(logdirectory):
        os.makedirs(logdirectory)
    return logdirectory


def create_robot_log_dir(projname, suite_name, dev_id, session):
    main_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    log_path = os.path.join(main_dir, "results")
    create_path = os.path.join(log_path, projname, suite_name, dev_id, session)
    print(f'create_path:{create_path}')
    gc.ROBOT_LOG_PATH = create_path

