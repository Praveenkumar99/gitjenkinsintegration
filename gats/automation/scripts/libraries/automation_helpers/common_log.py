# added to suppress the pylint error related to print in python 3
import os
import logging
import sys
import log_utils as log_utils

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

log = logging.getLogger(__name__)
#ROOT_LOG = ""


class common_log(object):
    ROOT_LOG = ""

    @staticmethod
    def return_values(boolean_val, log_type, log_msg):
        """
        Used to return boolean value  along with proper message
        :param boolean_val:  boolean value
        :param log_type:  defines log level(info/error)
        :param log_msg: Log message
        :return: boolean, log message
        Author : s.nandimandalam@globaledgesoft.com
        """
        if not isinstance(boolean_val, bool):
            raise Exception("{0} parameter is not valid".format(boolean_val))
        if boolean_val is False and log_type == "error":
            log.error(log_msg)
            return False, log_msg
        if boolean_val is False and log_type == "info":
            log.info(log_msg)
            return False, log_msg
        if boolean_val is False and log_type == "warning":
            log.warning(log_msg)#&{dict}     project=${1}     milestone=${2}     session=${3}     device=${4}    yaml=${5}    test_iter_count=${6}    testcase_name_and_iter_path=${7}    iteration_path=${8}
#&{dict}     project=${1}   
            return False, log_msg
        if boolean_val is True and log_type == "error":
            log.error(log_msg)
            return True, log_msg
        if boolean_val is True and log_type == "warning":
            log.warning(log_msg)
            return True, log_msg
        if boolean_val is False and log_type == "debug":
            log.debug(log_msg)
            return False, log_msg
        return True, log_msg

    @staticmethod
    def setup_logging(project, session, device, iter_count, suite, auto_id):
        """
        Generates script level logs
        :param project: Project name
        :param milestone: Milestone name
        :param session: Session name
        :param device: Device name
        :param suite: Suite name
        :param auto_id: Automation id(test case id)
        :return: h.vinay@globaledgesoft.com
        """
        print("Inside common log:",project, session, device, iter_count, suite, auto_id)
        common_log.ROOT_LOG = log_utils.setup_logging(auto_id, project,
                                                     session, device,
                                                       suite, iter_count)

    @staticmethod
    def remove_script_log_handler():
        """
        Removes all the logging handlers
        :return: None
        """
        log.debug("Inside remove_script_log_handler")
        log.info(common_log.ROOT_LOG.handlers)
        del common_log.ROOT_LOG.handlers[1:]
