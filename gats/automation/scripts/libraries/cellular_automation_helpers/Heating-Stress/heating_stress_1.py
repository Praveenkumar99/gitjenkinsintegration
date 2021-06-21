import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
import linecache

# Redirecting logs
log = logging.getLogger(__name__)

class perf_call:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def curr_temp(self, temp) -> int:
        line = linecache.getline(f"{gc.IMAGE_FOLDER}/phone_temp.txt", 1)
        val = int(line[-4:])
        return val

    def check_temp(self) -> float:
        temp_cmd = f"adb -s {self.Data['serialId']} shell dumpsys battery | grep \"temperature\" > {gc.IMAGE_FOLDER}/phone_temp.txt"
        (output, error, status) = cf.execute_commands(temp_cmd)
        temp = (self.curr_temp(gc.IMAGE_FOLDER)) / 10
        return temp

    def execute_test(self):
        log.info("Entering into Stress-Multitasking Block")
        log.info("Checking temperature of phone..")
        temp = self.check_temp()
        log.debug("Initial phone temperature =======> {0}'c".format(temp))

        if not temp <= 38:
            log.info("Due to phone ({0}'c)high temperature. The test case has stopped".format(temp))

        else:
            log.info("Initial phone temperature  is {0}'c".format(temp))

            log.info("Opening Game Application..")

            cmd = f"adb -s {self.Data['serialId']} shell am start -n game.freakx.monstersup/game.freakx.monstersup.MainActivity"
            (output, error, status) = cf.execute_commands(cmd)

            log.debug("Opening Game Application ======> {0}".format(cmd))
            time.sleep(2)

            num = 1
            while num <= 5:
                log.info("VOLTE CAll ========> {0}".format(num))
                log.info("Calling to device A..")
                cmd = f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][0]} shell am start -a android.intent.action.CALL -d tel:{self.Data['testcase_config'][self.tst]['callA_no']}"
                (output, error, status) = cf.execute_commands(cmd)
                log.debug("Calling to device A ======> self.Data['serialId']".format(cmd))
                time.sleep(5)

                status, mCallState = cf.fetch_call_state(gc.IMAGE_FOLDER,
                                                         self.Data['testcase_config'][self.tst]["callA_no"])
                if mCallState == 1 and status == True:
                    call_attend = f"adb -s {self.Data['serialId']} shell input keyevent 5"
                    (output, error, status) = cf.execute_commands(call_attend)
                    log.info("Call attended successfully from A side")
                    status, msg = cf.sleep(20, self.Data['serialId'], gc.IMAGE_FOLDER)
                    if not status:
                        log.info("Call got disconnected !!")
                        log.debug("Call got disconnected !!")
                        log.info("Terminating the call of B")
                        return False, "TestCase Failed"

                    disconnect_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 6"
                    (output, error, status) = cf.execute_commands(disconnect_cmd)
                    log.debug("Terminating the call of B ======> {0}".format(disconnect_cmd))
                    time.sleep(6)
                    temp = self.check_temp()
                    if not temp <= 38:
                        log.info(
                            "Due to phone ({0}'c) high temperature. The test cases has stopped".format(temp))
                        log.info("Checking current temperature.... self.Data['serialId']'c".format(temp))
                        num += 1

                    else:
                        disconnect_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 6"
                        (output, error, status) = cf.execute_commands(disconnect_cmd)
                        log.debug("A Terminating the call of B ======> {0}".format(disconnect_cmd))

                    disconnect_cmd = f" adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][0]} shell input keyevent 6"
                    (output, error, status) = cf.execute_commands(disconnect_cmd)
                    log.debug("A Terminating the call of B ======> {0}".format(disconnect_cmd))

                else:
                    log.info(f"Call is not received in device A")
                    disconnect_cmd = f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][0]} shell input keyevent 6"
                    (output, error, status) = cf.execute_commands(disconnect_cmd)

                time.sleep(8)
                close_cmd = f"adb -s {self.Data['serialId']} shell am force-stop game.freakx.monstersup"
                (output, error, status) = cf.execute_commands(close_cmd)
                log.debug("Closing the game application ======> {0}".format(close_cmd))

                log.info("Closing Game app...")

            log.info("Checking temperature of phone..")
            temp = self.check_temp()
            log.info("Final phone temperature =======> {0}'c".format(temp))
            log.debug("Final phone temperature =======> {0}'c".format(temp))

        log.info("Stress-Multitasking performed successfully")
        return True, " Stress-Multitasking performed successfully"


def game_cal_temp(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"], gc.IMAGE_FOLDER)
    if noOfDevices >= 2:
        call_obj = perf_call(tst, yamlData)
        status, msg = call_obj.execute_test()
    else:
        return False, "Two Devices are needed to execute the test case, {0} devices are connected".format(noOfDevices)
    return status, msg
