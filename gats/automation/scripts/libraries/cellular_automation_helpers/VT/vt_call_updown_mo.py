import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class Upgrade:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_call(self):
        log.info("Making VT Call to perform Up/Downgrade on VT call")
        log.info("Performing VT call from MO to MT")

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
            return False, "Call not received in devices B"

        log.info("Receiving call in device B")
        status, msg = adb.accept_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg

        log.info("Call attended successfully")

        # Downgrading the VT call
        status, msg = adb.downgrade_call(self.Data["serialId"])

        if not status:
            return False, msg

        status, msg = adb.lock_screen(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        if not status:
            return False, f"Locking Screen failed MT side due to {msg}"

        # Upgrading the VT call
        status, msg = adb.upgrade_call(self.Data["serialId"])

        if not status:
            return False, "Tapping on Video call failed"

        # Accepting the VT Call
        status, coordinates = cf.xml_file_parser("Answer with my video off",
                                                 self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                                 gc.IMAGE_FOLDER)

        if not status:
            return False, "Fetching the coordinates for Accepting the video call failed"

        status, msg = adb.tap_command(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                      x=coordinates[0] - 257,
                                      y=coordinates[1])

        if not status:
            return False, "Accepting the Video Call failed."

        time.sleep(5)

        # Terminating Call
        status, msg = adb.terminate_call(self.Data["serialId"])

        if not status:
            return False, "Call not Disconnected @ MO side"

        time.sleep(2)

        return True, "Call downgrade upgrade performed MO Successfully"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def vt_call_updown_mo(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Upgrade(tst, yamlData)
        status, msg = call_obj.execute_call()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg
