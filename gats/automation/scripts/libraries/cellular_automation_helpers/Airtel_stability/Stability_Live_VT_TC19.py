import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
import cellular_automation_helpers.common_helper_functions.ui_automator as ui
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class Vt_updown_mo:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_vt_updown(self):
        log.info("Performing Volte call from Device A")

        adb.lock_screen(self.Data["serialId"])
        adb.lock_screen(self.Data['testcase_config'][self.tst]["tempDevicesId"][0])

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
        
        if not status:
            return False, "Unable to accept call"

        time.sleep(1)

        # downgrade the VT call
        log.info("VT Call Downgrade Successfully")
        status, msg = ui.downgrade_call(self.Data["serialId"])

        if not status:
            return False, msg

        time.sleep(1)

        # Upgrading the Volte call
        status, msg = ui.upgrade_call(self.Data["serialId"])

        if not status:
            return False, "Tapping on Video call failed"

        log.info("Volte Call upgarding")
        
        status, msg = ui.acceptVT_call(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        
        if not status:
            return False, "VT call accepted failed"
        
        log.info("Volte call upgrade successfully")

        status, msg = cf.concurrency_call(  
                        5,
                        self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
                        self.Data['testcase_config'][self.tst]["callA_no"])
                    
        if not status:
            return False, "Call in between disconnected"

        # Terminating Call
        status, msg = adb.terminate_call(self.Data["serialId"])

        if not status:
            return False, "Call not Disconnected @ MO side"

        return True, "Call downgrade upgrade performed MO Successfully"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def grade1_vt(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Vt_updown_mo(tst, yamlData)
        status, msg = call_obj.execute_vt_updown()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg


