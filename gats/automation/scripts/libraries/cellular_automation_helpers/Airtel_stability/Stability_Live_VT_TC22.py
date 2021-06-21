import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
import cellular_automation_helpers.common_helper_functions.ui_automator as ui
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class Up_mo_down_mt:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_vt_updown(self):
        log.info("Performing Vt call from Device MO")
        
        status, msg = adb.lock_screen(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        if not status:
            return False, f"Locking Screen failed B side due to {msg}"
        
        # Calling B from A device and Accept call in B
        status, msg = adb.perform_a2b_vt_call(deviceId1=self.Data['serialId'],
                                           deviceId2=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                           callA=self.Data['testcase_config'][self.tst]['callA_no'],
                                           callB=self.Data['testcase_config'][self.tst]['callB_no'])

        if not status:
            return False, msg

        log.info("Call Accepted Successfully in MT")

        # downgrade the VT call
        log.info("MT downgrading the call ")
        status, msg = ui.downgrade_call(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg

        # Upgrading the MO Volte call
        log.info("Mo Upgrading the call")
        status, msg = ui.upgrade_call(self.Data["serialId"])

        if not status:
            return False, "Tapping on Video call failed"

        # Accepting the VT Call
        status, msg = ui.acceptVT_call(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg
        
        log.info("Vt call upgrade successfully")
        
        time.sleep(1)

        # Terminating Call
        status, msg = adb.terminate_call(self.Data["serialId"])

        if not status:
            return False, "Call not Disconnected @ MO side"

        return True, "Call downgrade upgrade performed Successfully"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def grade4_vt(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Up_mo_down_mt(tst, yamlData)
        status, msg = call_obj.execute_vt_updown()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg