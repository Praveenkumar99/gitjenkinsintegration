import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class OnHold:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_call(self):
        log.info("==Making a VT call from MT to MO to put call on Hold to Unhold==")

        # locking the screen of both devices.
        status, msg = adb.lock_screen(self.Data['serialId'])
        if not status:
            return False, f"Locking Screen failed MO side due to {msg}"

        status, msg = adb.lock_screen(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        if not status:
            return False, f"Locking Screen failed MT side due to {msg}"

        log.info("MO and MT devices both locked")

        # Triggering the VT Call from Device MT
        status, msg = adb.trigger_vt_call(
            deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
            phoneNumber=self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, msg

        # fetching the VT call state of Devices MO
        status, mCallState = adb.check_call_state(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callB_no"]
        )

        if not status:
            return False, mCallState

        # Receiving the Vt Call in MO side
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "Call not received in devices B"

        log.info("Receiving call in device B")
        status, msg = adb.accept_call(deviceId=self.Data['serialId'])

        if not status:
            return False, msg

        log.info("Call attended successfully @ MT side")

        # Fetching the Coordinates for Hold button
        log.info("=Fetching the Coordinate from the .xml file On A Device=")
        status, coordinates = cf.xml_file_parser("Hold", self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, "Dumping coordinates Hold failed"

        log.info("=Taping on Hold button=")

        status, msg = adb.tap_command(
            self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
            coordinates[0],
            coordinates[1])

        if not status:
            return False, "Tapping on hold button failed"

        # Fetching the Coordinates for Un - Hold button
        log.info("Fetching the Coordinates for Un hold")
        status, coordinates = cf.xml_file_parser("Hold", self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, "Dumping coordinates for Un hold button failed"

        log.info(f"=Tapping on Un-hold= {coordinates}")
        status, msg = adb.tap_command(self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                      coordinates[0], coordinates[1])

        if not status:
            return False, "Tapping on hold button failed"

        # Disconnecting the VT Call
        log.info("Terminating VT call @ MO side")
        status, msg = adb.terminate_call(deviceId=self.Data['serialId'])
        if not status:
            return False, msg

        return True, "Hold Performed Successfully @ MT"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def vt_mt_hold(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = OnHold(tst, yamlData)
        status, msg = call_obj.execute_call()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg

