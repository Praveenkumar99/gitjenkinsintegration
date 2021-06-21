import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)
#log = logging.getLogger('info_log')


class perf_VT_call:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_call(self):
        
        log.info("Entering into CALL Block")
        for loop in range(1):
            log.info(f"Start of Iteration : {loop + 1}")
            log.info("Calling to device B")
            cmd = f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.CALL -d tel:{self.Data['testcase_config'][self.tst]['callB_no']} --ei android.telecom.extra.START_CALL_WITH_VIDEO_STATE 3"
            log.debug(f"Calling from device A ===> {cmd}")
            (output, error, status) = cf.execute_commands(cmd)
            time.sleep(10)
            cmd = f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][0]} shell dumpsys telephony.registry | grep \"mCallState\|mCallIncomingNumber\" > {gc.IMAGE_FOLDER}/dump.txt"
            log.debug("Checking device B Call State ===> {0}".format(cmd))
            (output, error, status) = cf.execute_commands(cmd)
            status, mCallState = cf.fetch_call_state(gc.IMAGE_FOLDER,
                                                     self.Data['testcase_config'][self.tst]["callA_no"])
            if mCallState == 1 and status == True:
                log.info("Receiving call in device B")
                call_attend = f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][0]} shell input keyevent 5"
                log.debug(f"Receiving call in device B ===> {call_attend}")
                (output, error, status) = cf.execute_commands(call_attend)
                log.info("Call Attended Successfully")
                status, msg = cf.sleep(10, self.Data["serialId"], gc.IMAGE_FOLDER, self.Data['testcase_config'][self.tst]["callA_no"])
                if not status:
                    log.info("Call got disconnected !!")
                    log.debug("Call got disconnected !!")
                    return False, "TestCase Failed"
                log.info("Calling to device C")
                cmd = f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.CALL -d tel:{self.Data['testcase_config'][self.tst]['callC_no']} --ei android.telecom.extra.START_CALL_WITH_VIDEO_STATE 3"
                log.debug(f"Calling from device A ===> {cmd}")
                (output, error, status) = cf.execute_commands(cmd)
                time.sleep(10)
                cmd = f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][1]} shell dumpsys telephony.registry | grep \"mCallState\|mCallIncomingNumber\" > {gc.IMAGE_FOLDER}/dump.txt"
                log.debug("Checking device C Call State ===> {0}".format(cmd))
                (output, error, status) = cf.execute_commands(cmd)
                status, mCallState = cf.fetch_call_state(gc.IMAGE_FOLDER,
                                                         self.Data['testcase_config'][self.tst]["callA_no"])
                if mCallState == 1 and status == True:
                    log.info("Receiving call in device C")
                    call_attend = f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][1]} shell input keyevent 5"
                    log.debug(f"Receiving call in device C ===> {call_attend}")
                    (output, error, status) = cf.execute_commands(call_attend)
                    log.info("Call Attended Successfully")
                    status, coordinates = cf.xml_file_parser("Merge calls", self.Data["serialId"],gc.IMAGE_FOLDER)
                    log.info("A Merging call of B and C ")
                    print(coordinates)
                    cmd = f"adb -s {self.Data['serialId']} shell input tap {str(coordinates[0] - 100)} {str(coordinates[1] - 100)}"
                    print(cmd)
                    (output, error, status) = cf.execute_commands(cmd)
                    log.debug("A Merging call of B and C ======> {0}".format(cmd))
                    #cf.sleep(300, self.Data["deviceID"])
                    status, msg = cf.sleep(10, self.Data["serialId"], gc.IMAGE_FOLDER, self.Data['testcase_config'][self.tst]["callA_no"])
                    if not status:
                        log.info("Call got disconnected !!")
                        log.debug("Call got disconnected !!")
                        return False, "TestCase Failed"
                    # A disconnect the VT Call of B
                    log.info("Terminating call in device A")
                    disconnect_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 6"
                    log.debug("Terminating call in device A ===> {0}".format(disconnect_cmd))
                    (output, error, status) = cf.execute_commands(disconnect_cmd)
                    disconnect_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 6"
                    log.debug("Terminating call in device A ===> {0}".format(disconnect_cmd))
                    (output, error, status) = cf.execute_commands(disconnect_cmd)
                    time.sleep(2)
                else:
                    log.info(f"Call is not received in device c")
                    disconnect_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 6"
                    (output, error, status) = cf.execute_commands(disconnect_cmd)

            else:
                log.info(f"Call is not received in device B")
                disconnect_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 6"
                (output, error, status) = cf.execute_commands(disconnect_cmd)
        log.info("Test case executed")
        return True, "Test Case executed"


def long_vt_conf1(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"], gc.IMAGE_FOLDER)
    if noOfDevices == 3:
        call_obj = perf_VT_call(tst, yamlData)
        status, msg = call_obj.execute_call()
    else:
        return False, "Two Devices are needed to execute the test case, {0} devices are connected".format(noOfDevices)
    return status, msg
