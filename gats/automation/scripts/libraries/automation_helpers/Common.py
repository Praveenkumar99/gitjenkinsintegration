# pylint: disable=W1202

# added to suppress the pylint error related to print in python 3
import os
import subprocess
import logging
import sys
import re

# This run time import is required for the robot fwk.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import automation_helpers.globalconstants as gc
from common_log import common_log
from YamlUtils import YamlUtils
import time
from datetime import datetime
from datetime import timedelta



log = logging.getLogger(__name__)


def camera_config_func(config_name):
    camera_config_dict = {
        "MUSIC_PLAYER_PACKAGENAME": ["Music","packageName"],
        "CAMERA_PACKAGE_NAME": ["Camcorder","CameraPackageName"],
        "GALLERY_PACKAGE_NAME": ["Gallery","GalleryPackageName"],
        "NOTIFICATION_INCOMING_CALL": ["Common", "NotificationIncomingCall"],
        "NOTIFICATION_INCOMING_MSG": ["Common", "NotifcationIncomingMsg"]
    }
    if config_name in camera_config_dict.keys():
        config_list = camera_config_dict.get(config_name)
        config_value = YamlUtils.read_yml(config_list[0], config_list[1])
        return config_value
    else:
        return False


class Common(object):

    def __init__(self):
        self.common = common_log()


    @staticmethod
    def execute_adb_devices():
        """
        Gets the list of devices attached
        :return adb_devices: list of devices available
        Author : v.halli@globaledgesoft.com
        """
        adb_devices = []
        cmd = "adb devices"
        process_res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()
        for line in process_res[0].decode("utf-8").split("\n"):
            if re.search("\d", line):
                adb_devices.append(line.split())
        print('adb device: {}'.format(adb_devices))
        return adb_devices

    @staticmethod
    def check_adb_devices():
        """
        This method checks if the selected device is connected or not.
        :return: True/False, message
        Author : v.halli@globaledgesoft.com
        """
        device_list = Common.execute_adb_devices()

        # element exists in list of list or not?
        device_status = any(gc.DEVICE_ID in sublist for sublist in device_list)
        if device_status:
            return common_log.return_values(True, "info",
                                            "Selected device:{0} is connected "
                                            "to "
                                            "host machine. Starting execution"
                                            "....".
                                            format(gc.DEVICE_ID))
        return common_log.return_values(False, "info",
                                        "Selected device:{0} is not connected "
                                        "to "
                                        "host machine. Terminating execution".
                                        format(gc.DEVICE_ID))
