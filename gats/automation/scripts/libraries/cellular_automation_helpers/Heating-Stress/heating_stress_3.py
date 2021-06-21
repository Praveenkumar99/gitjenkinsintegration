import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)

import time


class Heating_stress:
    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def test_for_heat(self):
        log.info("==Heat Stress testing On MO devices==")

        # locking the screen
        status, msg = adb.lock_screen(self.Data['serialId'])
        if not status:
            return False, f"Locking Screen failed MO side due to {msg}"

        status, msg = adb.lock_screen(self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        if not status:
            return False, f"Locking Screen failed MT side due to {msg}"

        log.info("MO and MT devices both locked")

        # Checking initially Devices temperature
        status, temp1 = adb.check_device_heat(self.Data['serialId'])

        if not status:
            return False, temp1

        temp1 = cf.getDeviceTemprature(gc.IMAGE_FOLDER)

        # Calling B devices from A
        status, msg = adb.perform_a2b_call(deviceId1=self.Data['serialId'],
                                           deviceId2=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                           callA=self.Data['testcase_config'][self.tst]['callA_no'],
                                           callB=self.Data['testcase_config'][self.tst]['callB_no'])

        if not status:
            return False, msg

        log.info("Call received in device in B")

        status = cf.sleep(self.Data['testcase_config'][self.tst]['Call_duration'],
                          self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                          mobileNumber=self.Data['testcase_config'][self.tst]['callA_no'])

        if not status:
            return False, "Call Disconnected in between MO and MT"

        # Disconnecting the Call
        log.info("=Disconnecting the call=")
        status, msg = adb.terminate_call(self.Data['serialId'])

        if not status:
            return False, "Disconnecting Call Failed"

        # opening Youtube
        (output, error, status) = cf.execute_commands("adb -s {0} shell am start -a android.intent.action.VIEW -d {1} "
                                                      "".format(self.Data["serialId"],
                                                                self.Data['testcase_config'][self.tst]["HTTPS_LINK"]))

        if not status:
            return False, "Opening the youtube failed"

        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['youtube_duration']

        while True:
            if time.time() > timeout:
                break
            (output, error, status) = cf.execute_commands(
                f"adb -s {self.Data['serialId']} shell input keyevent KEYCODE_MEDIA_NEXT")

            if not status:
                return False, "Browsing the youtube video failed"

            time.sleep(5)

        # Making Video call for 30 min
        status, msg = adb.perform_a2b_vt_call(deviceId1=self.Data['serialId'],
                                              deviceId2=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                              callA=self.Data['testcase_config'][self.tst]['callA_no'],
                                              callB=self.Data['testcase_config'][self.tst]['callB_no'])

        if not status:
            return False, msg

        status = cf.sleep(1800,
                          self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                          mobileNumber=self.Data['testcase_config'][self.tst]['callA_no'])

        if not status:
            return False, "Vt Call disconnected in between "

        log.info("=Disconnecting the VT call=")
        status, msg = adb.terminate_call(self.Data['serialId'])

        if not status:
            return False, "Disconnecting VT call Failed"

        # Checking initially Devices temperature
        status, temp2 = adb.check_device_heat(self.Data['serialId'])

        if not status:
            return False, temp2

        if not status:
            return False, "Measuring the Final tempreture command failed"

        temp2 = cf.getDeviceTemprature(gc.IMAGE_FOLDER)
        log.info(f'Initial Tempreture {temp1}, Final Tempreture {temp2}')

        return True, "Heat Check Performed Successfully"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def perform_heat_stress_3(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"], gc.IMAGE_FOLDER)
    if noOfDevices >= 2:
        call_obj = Heating_stress(tst, yamlData)
        status, msg = call_obj.test_for_heat()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)
    if not status:
        call_obj.closeUp()
    return status, msg
