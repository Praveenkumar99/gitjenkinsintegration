import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)
#log = logging.getLogger('info_log')


class perform_volte_conf_call:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_volte_conf_call(self):

        log.info("Performing Volte call in device A to device B")

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

        log.info("Call attended successfully in device B")

        log.info("Checking Concurrency of the call for 10 seconds")
        status, msg = cf.concurrency_call(
            10,
            self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
            self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, "Call got disconnected!!!"

        log.info("Performing Volte call in device C to device A")

        # Triggering the Call from Device C
        status, msg = adb.trigger_volte_call(
            deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][1],
            phoneNumber=self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, msg

        # fetching the call state of Device A
        status, mCallState = adb.check_call_state(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callC_no"]
        )

        if not status:
            return False, mCallState

        # Receiving the Call in Device A
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "Call not received in device A"

        log.info("Receiving call in device A")
        status, msg = adb.accept_call(deviceId=self.Data['serialId'])

        if not status:
            return False, msg

        log.info("Call attended successfully in device A received from device C")

        log.info("Checking Concurrency of the call for 10 seconds")
        status, msg = cf.concurrency_call(
            10,
            self.Data['testcase_config'][self.tst]["tempDevicesId"][1],
            self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, "Call got disconnected!!!"
            
        status, coordinates = cf.xml_file_parser("Merge", self.Data["serialId"])

        log.info("A Merging call of B and C ")
        status, msg = adb.tap_command(self.Data['serialId'], str(coordinates[0]), 
            str(coordinates[1]))

        if not status:
            return False, "Unable to merge the calls"
        
        log.info("Checking Concurrency of the call for 3600 seconds")
        status, msg = cf.concurrency_call(
            3600,
            self.Data["serialId"],
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
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][1])


def conf_2(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])
    if noOfDevices >= 3:
        call_obj = perform_volte_conf_call(tst, yamlData)
        status, msg = call_obj.execute_volte_conf_call()
    else:
        return False, "Two Devices are needed to execute the test case, {0} devices are connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg
