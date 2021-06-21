# Reboot the devices.
import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class RebootDevice:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute(self):
        # rebooting the devices
        log.info("Rebooting the device")
        status, msg = adb.rebootDevice(deviceId=self.Data['serialId'])

        if not status:
            return False, msg
        # Waiting for devices to reboot
        timeout = time.time() + self.Data['testcase_config'][self.tst]['reboot_duration']

        while True:
            if time.time() >= timeout:
                break
        
        # validating the Ims registration
        status, msg = adb.imsRegistrationValidator(deviceId=self.Data['serialId'])

        print(msg)

        if status:
            # Testcase passed waiting for 2 min start next iteration.
            timeout = time.time() + 3

            while True:
                if time.time() >= timeout:
                    break
            return True, "Testcase passed"

        # Test case failed waiting for 2 min
        timeout = time.time() + 15 * 2

        while True:
            if time.time() >= timeout:
                break

        # second time validating the Ims registration
        status, msg = adb.imsRegistrationValidator(deviceId=self.Data['serialId'])

        if not status:
            return False, "Ims registration failed"
        return True, "Second Time Ims registration done"


def reboot_attach_validation(tst, yamlData):
    call_obj = RebootDevice(tst, yamlData)
    status, msg = call_obj.execute()

    return status, msg
