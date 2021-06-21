import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
from uiautomator import Device


# Redirecting logs
log = logging.getLogger(__name__)


class Volte_updown_mt:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_volte_updown(self):
        log.info("Making Volte Call to perform Up/Downgrade on Volte call")
        log.info("Performing Volte call from A to B")

        # Triggering the Call from Device B
        status, msg = adb.trigger_volte_call(
            deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
            phoneNumber=self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, msg

        # fetching the call state of Devices B
        status, mCallState = adb.check_call_state(
            deviceId=self.Data["serialId"],
            phoneNumber=self.Data['testcase_config'][self.tst]["callB_no"]
        )

        if not status:
            return False, mCallState

        # Receiving the Call in Devices A
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "Call not received in devices B"

        log.info("Receiving call in device A")
        status, msg = adb.accept_call(deviceId=self.Data["serialId"])

        if not status:
            return False, msg

        log.info("Call attended successfully")

        time.sleep(3)

        status, msg = adb.lock_screen(self.Data["serialId"])

        if not status:
            return False, f"Locking Screen failed B side due to {msg}"

        # Upgrading the Volte call
        status, msg = adb.upgrade_call(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, "Tapping on Video call failed"

        # status, msg_1 = adb.downgrade_call(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        # print(msg)

        # swip up to answer the VT Call
        status, msg = adb.swipe_up(self.Data['serialId'])

        time.sleep(3)
        if not status:
            return False, "Accepting the Video Call failed."

        # downgrade the VT call
        status, msg = adb.downgrade_call(self.Data['serialId'])
        
        if not status:
            return False, msg

        time.sleep(5)

        # Terminating Call in Devices B
        status, msg = adb.terminate_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, "Call not Disconnected @ MO side"

        time.sleep(2)

        return True, "Call downgrade upgrade performed MT Successfully"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
          
  
def volte_up_down_mt(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Volte_updown_mt(tst, yamlData)
        status, msg = call_obj.execute_volte_updown()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg

