import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class AeroplaneMode:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute(self):
        # Aeroplane Mode On the devices
        log.info("Toggling aeroplane mode in the device")
        status, msg = cf.toggle_airplane_mode(deviceId=self.Data['serialId'])

        if not status:
            return False, msg

        # Waiting for devices to reboot
        # timeout = time.time() + self.Data['testcase_config'][self.tst]['reboot_duration']
        # print(timeout)
        # print(time.time())
        # while True:
        #     if time.time() >= timeout:
        #         break

        # validating the Ims registration
        status, msg = adb.imsRegistrationValidator(deviceId=self.Data['serialId'])

        if status:
            # Testcase passed waiting for 2 min start next iteration.
            timeout = time.time() + 60 * 2
            
            while True:
                if time.time() >= timeout:
                    break
            return True, "Testcase passed"

        # Test case failed waiting for 2 min
        log.info("Failed to attach, Waiting For 2 mins!!!")
        timeout = time.time() + 60 * 2
        

        while True:
            if time.time() >= timeout:
                break

        # second time validating the Ims registration
        status, msg = adb.imsRegistrationValidator(deviceId=self.Data['serialId'])

        if not status:
            return False, "Ims registration failed"

def apm_attach_validation(tst, yamlData):
    call_obj = AeroplaneMode(tst, yamlData)
    status, msg = call_obj.execute()
    print(status, msg)
    # Validating Test case result
    return status, msg
