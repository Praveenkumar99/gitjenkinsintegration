import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)

class Perform_vt_call_reject:

    def __init__(self,tst, yamlData):
        self.tst = tst
        self.Data = yamlData
    
    def execute_call(self):
        log.info("Performing VT call")

        # Triggering the Call from Device A
        status, msg = adb.trigger_vt_call(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callB_no"])

        if not status:
            return False, msg

        # fetching the call state of Devices B
        status, mCallState = adb.check_call_state(
            deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
            phoneNumber=self.Data['testcase_config'][self.tst]["callA_no"]
        )

        if not status:
            return False, mCallState

        # Receiving the Call in Devices B
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "Call not received in device B"
        
        # Disconnecting the Call
        log.info("Terminating call in device B")
        status, msg = adb.terminate_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        if not status:
            return False, msg

        log.info("Test case executed")
        return True, "Test Case executed"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def reject_vt(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Perform_vt_call_reject(tst, yamlData)
        status, msg = call_obj.execute_call()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg
