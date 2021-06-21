import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class Volte_updown_mo:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_volte_updown(self):
        log.info("Performing Volte call from Device A")
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
        
        time.sleep(3)

        status, msg = adb.lock_screen(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, f"Locking Screen failed B side due to {msg}"

        # Upgrading the Volte call
        status, msg = adb.upgrade_call(self.Data["serialId"])

        if not status:
            return False, "Tapping on Video call failed"

        status, msg_1 = adb.downgrade_call(self.Data["serialId"])

        print(msg)

        # Accepting the VT Call
        status, coordinates = cf.xml_file_parser("Answer with my video off",
                                                 self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, "Fetching the coordinates for Accepting the video call failed"

        status, msg = adb.tap_command(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                      x=coordinates[0] - 257,
                                      y=coordinates[1])

        if not status:
            return False, "Accepting the Video Call failed."

        # downgrade the VT call
        #status, msg = adb.downgrade_call(self.Data["serialId"])
        status, msg = adb.tap_command(deviceId=self.Data["serialId"],
                                      x=msg_1[0] - 67,
                                      y=msg_1[1] - 63)
        status, msg = adb.tap_command(deviceId=self.Data["serialId"],
                                      x=msg_1[0] - 67,
                                      y=msg_1[1] - 63)

        if not status:
            return False, msg

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


def volte_up_down_mo(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Volte_updown_mo(tst, yamlData)
        status, msg = call_obj.execute_volte_updown()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg
