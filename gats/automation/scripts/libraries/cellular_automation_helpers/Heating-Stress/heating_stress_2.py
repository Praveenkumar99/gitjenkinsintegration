import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
# Redirecting logs
log = logging.getLogger(__name__)


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

        # Calling B from A device and Accept call in B
        status, msg = adb.perform_a2b_call(deviceId1=self.Data['serialId'],
                                           deviceId2=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
                                           callA=self.Data['testcase_config'][self.tst]['callA_no'],
                                           callB=self.Data['testcase_config'][self.tst]['callB_no'])

        if not status:
            return False, msg

        log.info("Call Accepted Successfully in MT")

        # Sending SMS
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['Call_duration']
        sms_limit = self.Data['testcase_config'][self.tst]['sms_count']

        while True:
            print(timeout)
            print(time.time())
            if time.time() > timeout:
                break
            if sms_limit == 0:
                time.sleep(5)
                continue

            log.info(f"Sending SMS {sms_limit - (sms_limit - 1)}")

            time.sleep(5)

            status, msg = adb.send_sms(self.Data['serialId'], self.Data['testcase_config'][self.tst]['callB_no'])
            if not status:
                return False, msg

        # Disconnecting the Call
        log.info("=Disconnecting the call=")
        status, msg = adb.terminate_call(self.Data['serialId'])

        if not status:
            return False, "Disconnecting Call Failed"

        # Checking initially Devices temperature
        status, temp1 = adb.check_device_heat(self.Data['serialId'])

        if not status:
            return False, temp1

        temp2 = cf.getDeviceTemprature(gc.IMAGE_FOLDER)
        log.info(f'Initial Tempreture {temp1}, Final Tempreture {temp2}')
        log.info(f"Tempreture Differences is {temp2 - temp1}")

        return True, "Heat Performed Successful"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def perform_heat_stress_2(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"], gc.IMAGE_FOLDER)
    if noOfDevices >= 2:
        call_obj = Heating_stress(tst, yamlData)
        status, msg = call_obj.test_for_heat()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    if not status:
        call_obj.closeUp()

    return status, msg
