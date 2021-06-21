#Ongoing volte call from A to B,add VT call from A to C

import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)

class perform_volte_call_vt:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_volte_call_vt(self):
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

        print("Checking Concurrency of the call for 10 seconds")
        status, msg = cf.concurrency_call(
            10,
            self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
            self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, "Call got disconnected!!!"

        log.info("Calling to device C")

        # Triggering the Call from Device A
        status, msg = adb.trigger_vt_call(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callC_no"])

        if not status:
            return False, msg

        # fetching the call state of Devices C
        status, mCallState = adb.check_call_state(
            deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][1],
            phoneNumber=self.Data['testcase_config'][self.tst]["callA_no"]
        )

        if not status:
            return False, mCallState

        # Receiving the Call in Devices C
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "Call not received in devices C"

        log.info("Receiving call in device C")
        status, msg = adb.accept_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][1])

        if not status:
            return False, msg

        log.info("Call attended successfully")

        print("Checking Concurrency of the call for 10 seconds")
        status, msg = cf.concurrency_call(
            10,
            self.Data['testcase_config'][self.tst]["tempDevicesId"][1],
            self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, "Call got disconnected!!!"

        # Disconnecting the Call
        log.info("Terminating call in device C")
        status, msg = adb.terminate_call(deviceId=self.Data['testcase_config'][self.tst]["tempDevicesId"][1])
        if not status:
            return False, msg

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
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][1])


def volte_vt_16(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])
    if noOfDevices >= 2:
        call_obj = perform_volte_call_vt(tst, yamlData)
        status, msg = call_obj.execute_volte_call_vt()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

# Validating Test case result
    if not status:
        call_obj.closeUp()
    print("Stopping logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

    return status, msg











































































































































