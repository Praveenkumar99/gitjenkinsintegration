import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class Up_mo_down_mt:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_volte_updown(self):
        log.info("Performing Volte call from Device MO")

        # Calling B from A device and Accept call in B
        status, msg = adb.perform_a2b_call(deviceId1=self.Data['serialId'],
                                           deviceId2=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                           callA=self.Data['testcase_config'][self.tst]['callA_no'],
                                           callB=self.Data['testcase_config'][self.tst]['callB_no'])

        if not status:
            return False, msg

        log.info("Call Accepted Successfully in MT")
        # Locking the devices
        status, msg = adb.lock_screen(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, f"Locking Screen failed B side due to {msg}"

        # Upgrading the MO Volte call
        log.info("Mo Upgrading the call")
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

        log.info("MO Upgraded the call Successfully")

        # downgrade the VT call
        log.info("MT downgrading the call ")
        status, msg = adb.downgrade_call(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg

        log.info("MT downgraded the call Successfully")
        time.sleep(5)

        # Terminating Call
        status, msg = adb.terminate_call(self.Data["serialId"])

        if not status:
            return False, "Call not Disconnected @ MO side"

        time.sleep(2)

        return True, "Call downgrade upgrade performed Successfully"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def volte_up_mo_down_mt(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Up_mo_down_mt(tst, yamlData)
        status, msg = call_obj.execute_volte_updown()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg