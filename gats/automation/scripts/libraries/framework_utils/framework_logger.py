import logging
import os


ROOT_LOG = logging.root
LOG = logging.getLogger(__name__)


class FrameworkLogger(object):
    """
             :class name : FrameworkLogger
             :description: Contains function api related to creation of
                           robot_result tree structure

    """
    @staticmethod
    def get_session(session_name):
        """

        :param session_name:
        :return:
        :author: s.subhodeep@globaledgesoft.com
        """
        main_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        log_path = os.path.join(main_dir, "results", "robot_results")
        return os.path.join(log_path, session_name)

    def make_robot_log_dir(self, *args):
        """

        :param args:
        :return:
        :author: s.subhodeep@globaledgesoft.com
        """
        os.path.join(args[0], args[1])
        log_directory = os.path.join(self.get_session(args[0]),
                                     args[1],
                                     args[2])
        return log_directory
