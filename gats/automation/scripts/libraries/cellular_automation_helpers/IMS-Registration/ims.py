import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)
#log = logging.getLogger('info_log')


def get_ims_reg_state(deviceId, outputPath):

    cmd = f"adb -s {deviceId} shell am start -a android.intent.action.VIEW -d tel:%2A%23%2A%234636%23%2A%23"
    (output, error, status) = cf.execute_commands(cmd)
    time.sleep(5)
    log.info("performing keyevent")
    cmd = f"adb -s {deviceId} shell input keyevent 17"
    (output, error, status) = cf.execute_commands(cmd)
    time.sleep(5)

    log.info("fetching coordinates for phone information")
    status, coordinates = cf.xml_file_parser("Phone information", deviceId, outputPath)
    print(coordinates)
    cmd = f"adb -s {deviceId} shell input tap {str(coordinates[0])} {str(coordinates[1])}"
    print(cmd)
    cf.execute_commands(cmd)
    time.sleep(5)

    log.info("fetching coordinates for more")
    status, coordinates = cf.xml_file_parser('"More', deviceId, outputPath)
    coordinate0 = coordinates[0] - 60
    coordinate1 = coordinates[1] - 60
    cmd = f"adb -s {deviceId} shell input tap {str(coordinate0)} {str(coordinate1)}"
    print(cmd)

    cf.execute_commands(cmd)
    time.sleep(5)

    log.info("fetching coordinates for ims service status")
    status, coordinates = cf.xml_file_parser("IMS Service Status", deviceId, outputPath)
    cmd = f"adb -s {deviceId} shell input tap {str(coordinates[0])} {str(coordinates[1])}"
    cf.execute_commands(cmd)
    time.sleep(5)

    log.info("fetching coordinates for ims registration")
    reg_state = cf.xml_file_parser1("IMS registration", deviceId, outputPath)
    log.info("IMS REGISTRATION STATE IS {0}".format(reg_state))
    time.sleep(5)

    cmd = f"adb -s {deviceId} shell input keyevent 4"
    cf.execute_commands(cmd)
    cmd = f"adb -s {deviceId} shell input keyevent 4"
    cf.execute_commands(cmd)
    cmd = f"adb -s {deviceId} shell input keyevent 4"
    cf.execute_commands(cmd)
    cmd = f"adb -s {deviceId} shell input keyevent 4"
    cf.execute_commands(cmd)
    cmd = f"adb -s {deviceId} shell input keyevent 4"
    cf.execute_commands(cmd)
    cmd = f"adb -s {deviceId} shell input keyevent 4"
    cf.execute_commands(cmd)
    cmd = f"adb -s {deviceId} shell input keyevent 4"
    cf.execute_commands(cmd)
    time.sleep(5)
    return reg_state


class ims_reg_dereg:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_ims_reg_dereg(self):
        log.debug("Checking for IMS registration state..")
        reg_state = get_ims_reg_state(self.Data["serialId"], gc.IMAGE_FOLDER)
        time.sleep(5)
        log.info("Entering into Airplane mode block..")
        status = cf.toggle_airplane_mode(self.Data["serialId"], gc.IMAGE_FOLDER)
        if int(status) == 1:
            log.info("Airplane mode is on...")
            reg_state = get_ims_reg_state(self.Data["serialId"], gc.IMAGE_FOLDER)
            if reg_state == ' Not Registered':
                log.info("Test case executed successfully for iteration")
            else:
                log.info("Test case execution failed ")
                return False, "TestCase failed"
        else:
                log.info("Airplane mode is off...")
                reg_state = get_ims_reg_state(self.Data["serialId"], gc.IMAGE_FOLDER)
                if reg_state == ' Registered':
                    log.info("Test case executed successfully for iteration")
                else:
                    log.info("Test case execution failed")
                    return False, "TestCase failed"
        log.info("TestCase Executed")
        return True, "TestCase Executed Succesfully"

def ims_reg_dereg_state(tst, yamlData):
    call_obj = ims_reg_dereg(tst, yamlData)
    status, msg = call_obj.execute_ims_reg_dereg()
    return status, msg
