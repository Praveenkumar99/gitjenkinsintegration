#During volte call send SMS from MO side and Receive MT side
import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)

class perform_call_send_sms:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_call_send_sms(self):

        log.info("Performing Volte call")

        # Triggering the Call from Device A
        status, msg = adb.trigger_volte_call(
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
            return False, "Call not received in devices B"

        log.info("Receiving call in device B")
        status, msg = adb.accept_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg

        log.info("Call attended successfully")

        print("Checking Concurrency of the call for 5 seconds")
        status, msg = cf.concurrency_call(
            5,
            self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
            self.Data['testcase_config'][self.tst]["callA_no"]
            )

        if not status:
            return False, "Call got disconnected!!!"
            
        # for loop in range(10):
        log.info("Sending sms from device A")
        status, msg = adb.send_sms(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callB_no"])

        if not status:
            return False, "Unable to send sms"

        print("Checking Concurrency of the call for 3 seconds")
        status, msg = cf.concurrency_call(
           3,
           self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
           self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
           return False, "Call got disconnected!!!"

        # Disconnecting the Call
        log.info("Terminating call in device A")
        status, msg = adb.terminate_call(deviceId=self.Data['serialId'])
        if not status:
            return False, msg

        log.info("Test case executed")
        return True, "Test Case executed"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

def volte_sms_1(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])
    if noOfDevices >= 2:
        call_obj = perform_call_send_sms(tst, yamlData)
        status, msg = call_obj.execute_call_send_sms()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg










































































