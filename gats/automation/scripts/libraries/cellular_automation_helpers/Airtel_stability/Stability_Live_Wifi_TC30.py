import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)

class perform_wifi_action:
    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_wifi_action(self):
        log.debug("==Entering into WiFi Block==")
        cmd = f"adb -s {self.Data['serialId']} logcat -c"
        (output, error, status) = cf.execute_commands(cmd)
        time.sleep(3)
        if not status:
            return False, "Not executed"
        log.info("Turn OFF WiFi...")
        cmd = f"adb -s {self.Data['serialId']} shell svc wifi disable"
        (output, error, status) = cf.execute_commands(cmd)
        time.sleep(3)
        if not status:
            return False, "WiFi is not turned OFF"

        log.info("Turn ON WiFi...")
        cmd = f"adb -s {self.Data['serialId']} shell svc wifi enable"
        (output, error, status) = cf.execute_commands(cmd)
        time.sleep(3)
        if not status:
           return False, "WiFi is not turned ON"
        return True, "Test case executed"

def wifi_enable_disable(tst, yamlData):
    
    wifi_obj = perform_wifi_action(tst, yamlData)
    status, msg = wifi_obj.execute_wifi_action()
   
    return status, msg
