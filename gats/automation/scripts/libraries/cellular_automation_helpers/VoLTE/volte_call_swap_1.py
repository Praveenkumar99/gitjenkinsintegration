import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class SwappingCall:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_call(self):
        log.info("==Performing Swap on A2B and A2C call==")

        log.info("==Making a call from A to B==")
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

        time.sleep(1)

        log.info("==Making a call from A to C keeping A and B call on hold==")
        # Triggering the Call from Device A to C
        status, msg = adb.trigger_volte_call(
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

        log.info("Call attended successfully in devices C")

        # Tapping on Swap button
        log.info("=Fetching the Coordinate from the .xml file On A Device=")
        status, coordinates = cf.xml_file_parser("Swap", self.Data['serialId'])

        if not status:
            return False, "Dumping coordinates for Swap failed"

        log.info("=Tapping on Swap button=")

        status, msg = adb.tap_command(self.Data['serialId'], coordinates[0], coordinates[1])

        if not status:
            return False, "Tapping on Swap button failed"

        # Disconnecting the Call A to B call
        log.info("Terminating A to B call in device A")
        status, msg = adb.terminate_call(deviceId=self.Data['serialId'])
        if not status:
            return False, msg

        # Disconnecting the Call A to B call
        log.info("Terminating A to C call in device A")
        status, msg = adb.terminate_call(deviceId=self.Data['serialId'])
        if not status:
            return False, msg

        return True, "Called Swapped Successfully in Device A"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][1])


def swap_1(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 3:
        call_obj = SwappingCall(tst, yamlData)
        status, msg = call_obj.execute_call()
    else:
        return False, "Three Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg
