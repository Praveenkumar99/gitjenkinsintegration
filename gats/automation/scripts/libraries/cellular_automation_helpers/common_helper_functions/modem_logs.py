import re
import os
import time
import logging
import subprocess
import datetime
from datetime import datetime
from automation_helpers.YamlUtils import YamlUtils
import automation_helpers.globalconstants as gc
import common_functions as cf

Log = logging.getLogger(__name__)

def delete_old_log(deviceId, logPath):
    Log.info("Deleting old pixel logs at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell rm {logPath}/*")
    time.sleep(5)
    Log.info("Deleted old pixel logs at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    return True, "Deleted old logs"


def start_pixel_logger(deviceId):
    """Staring the pixel logger Application
    """
    cmd = "adb -s {0} shell am start -n com.android.pixellogger/com.android.pixellogger.ui.main.MainActivity > logger.txt".format(deviceId)
    (output, error, status) = cf.execute_commands(cmd)
    time.sleep(3)
    if status == True:
        with open("logger.txt",'r') as f:
            for l in f.readlines() :
                if "Error:" in l:
                    Log.info("error while running the pixel logger!!!")
                    f.close()
                    (output, error, status) = cf.execute_commands("rm logger.txt")
                    return False, 'Unable to open pixel logger apk'
                else :
                    f.close()
                    (output, error, status) = cf.execute_commands("rm logger.txt")

            (output, error, status) = cf.execute_commands("adb -s {0} shell input tap 960 1984".format(deviceId))
    else :
        return False, 'Unable to open pixel logger apk'
    Log.info("Starting pixel logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    time.sleep(20)
    Log.info("Pixel logger is started at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    return True, 'Pixel logger has been started'

def stop_pixel_logger(deviceId, outputPath):
    """Stopping the Pixel logger application
    """
    (output, error, status) = cf.execute_commands("adb -s {0} shell am start -n com.android.pixellogger/com.android.pixellogger.ui.main.MainActivity".format(deviceId))
    time.sleep(3)
    Log.info("stopping pixel logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    (output, error, status) = cf.execute_commands("adb -s {0} shell input tap 960 1984".format(deviceId))
    time.sleep(25)
    (output, error, status) = cf.execute_commands("adb -s {0} shell am force-stop com.android.pixellogger > logger.txt".format(deviceId))

    if status == True :
        with open("logger.txt",'r') as f :
            for l in f.readlines() :
                if "Error:" in l :
                    Log.info("error while stopping the pixel logger!!!")
                    f.close()
                    (output, error, status) = cf.execute_commands("rm logger.txt")
                    return False, 'error while stopping the pixel logger!!!'
                else :
                    f.close()
                (output, error, status) = cf.execute_commands("rm logger.txt")
        Log.info("Pixel logger is stopped at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

        (output, error, status) = cf.execute_commands("adb -s {0} pull /storage/emulated/0/Android/data/com.android.pixellogger/files/logs/diag_logs/ {1}/{0}".format(deviceId, outputPath))
        time.sleep(5)
        (output, error, status) = cf.execute_commands(" adb -s {0} shell rm /storage/emulated/0/Android/data/com.android.pixellogger/files/logs/diag_logs/*".format(deviceId))
        time.sleep(5)
        Log.info("Logs are moved to output folder at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        return True, 'Pixel logger is stopped'
    else :
        return False, "error while stopping the pixel logger!!!"
def start_oneplus_logger(deviceId):
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell am start -a android.intent.action.VIEW -d tel:%2A%23800")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input keyevent 18")
    if not status:
        return False, "Issue in opening log Collection"
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input keyevent 22")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input keyevent 22")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input keyevent 66")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input tap 830 584")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input tap 830 1503")
    Log.info("Starting logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

    return True, "Initiated Logs"

def stop_oneplus_logger(deviceId, outputPath):
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell am start -a android.intent.action.VIEW -d tel:%2A%23800")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input keyevent 18")
    if not status:
        return False, "Issue in opening log Collection"
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input tap 830 584")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input tap 830 1383")
    Log.info("Stopping logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    (output, error, status) = cf.execute_commands("adb -s {0} pull /storage/emulated/0/oem_logs/diag_logs/ {1}/{0}".format(deviceId, outputPath))
    time.sleep(5)
    (output, error, status) = cf.execute_commands(" adb -s {0} shell rm /storage/emulated/0/oem_logs/diag_logs/*".format(deviceId))
    time.sleep(5)
    Log.info("Logs are moved to output folder at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    return True, "Stopped Log collection"

def mi_logger(deviceId, str1, outputPath):
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell am start -n com.android.settings/.SubSettings")
    if not status:
        return False, ""
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input touchscreen swipe 546 2241 546 260")
    time.sleep(2)
    status, coOrdinates = xml_file_parser("Services &amp; feedback", deviceId, gc.IMAGE_FOLDER)
    cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
    (output, error, status) = cf.execute_commands(cmd)
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input tap 967 188")

    status, coOrdinates = cf.xml_file_parser("Generate logs", deviceId, gc.IMAGE_FOLDER)
    if not status:
        return False, "Issue in generating Logs"
    cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
    (output, error, status) = cf.execute_commands(cmd)


    if str1 == "ON":
        Log.info("Starting logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        status, coOrdinates = xml_file_parser("Generate logs", deviceId,gc.IMAGE_FOLDER)
        cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
        (output, error, status) = cf.execute_commands(cmd)
        (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input tap 967 188")

    elif str1 == "OFF":
        Log.info("Stopping logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        status, coOrdinates = xml_file_parser("Finish and upload", deviceId, gc.IMAGE_FOLDER)
        cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
        (output, error, status) = cf.execute_commands(cmd)
        (output, error, status) = cf.execute_commands("adb -s {0} pull /storage/emulated/0/diag_logs/ {1}/{0}".format(deviceId, outputPath))
        time.sleep(5)
        (output, error, status) = cf.execute_commands(" adb -s {0} shell rm /storage/emulated/0/diag_logs/*".format(deviceId))
        time.sleep(5)
        Log.info("Logs are moved to output folder at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

    return True, "Logger is {0}".format(str1)

def start_log(devName, devId):
    #import pdb;pdb.set_trace()
    if devName[0:-3] == "MI_10T":
        status, msg = mi_logger(devId, "ON")
    elif devName[0:-3] == "One_Plus":
        status, msg = start_oneplus_logger(devId)
    elif devName[0:-3] == "GooglePixel":
        status, msg = start_pixel_logger(devId)
    else:
        return False, "Device name Not Recognised!!!"

    return status, msg

def stop_log(devName, devId, outputPath):
    if devName[0:-3] == "MI_10T":
        status, msg = mi_logger(devId, "OFF", outputPath)
    elif devName[0:-3] == "One_Plus":
        status, msg = stop_oneplus_logger(devId, outputPath)
    elif devName[0:-3] == "GooglePixel":
        status, msg = stop_pixel_logger(devId, outputPath)
    else:
        return False, "Device name Not Recognised!!!"
    return status, msg

def delete_log(devName, devId):
    if devName[0:-3] == "MI_10T":
        status, msg = delete_old_log(devId, "/storage/emulated/0/diag_logs")
    elif devName[0:-3] == "One_Plus":
        status, msg = delete_old_log(devId, "/storage/emulated/0/oem_logs/diag_logs")
    elif devName[0:-3] == "GooglePixel":
        status, msg = delete_old_log(devId, "/storage/emulated/0/Android/data/com.android.pixellogger/files/logs/diag_logs")
    else:
        return False, "Device name Not Recognised!!!"

    return status, msg

def logcat_initialize(devicesId):
    Log.info("Initating Logcat")
    for device in devicesId:
        (output, error, status) = cf.execute_commands(f"adb -s {device} logcat {gc.IMAGE_FOLDER}/{device}_logcat.txt")

    if not status:
        return False, "Logcat is not initiated"

    return True, "Logcat is initiated successfully"

def logcat_stop(devicesId):
    Log.info("Stopping Logcat")
    for device in devicesId:
        (output, error, status) = cf.execute_commands(f"ps -ef | grep 'logcat' > {gc.IMAGE_FOLDER}/logcat_dump.txt")
        with open(f"{gc.IMAGE_FOLDER}/logcat_dump.txt", "r") as fd:
            data = fd.readlines()
            for line in data:
                if device in line:
                    processId = [int(s) for s in line.split(" ") if s.isdigit()]
                    (output, error, status) = cf.execute_commands(f"kill -9 {processId[1]}")
        (output, error, status) = cf.execute_commands(f"rm {gc.IMAGE_FOLDER}/logcat_dump.txt")

    if not status:
        return False, "Logcat is not Stopped"

    return True, "Logcat is stopped successfully"

def modem_logging(yamlData, tst, log_type, log_status):

    devicesId = []
    devicesNames = []
    devicesId.append(yamlData["serialId"])
    devicesNames.append(yamlData["deviceName"])

    if log_status == "START":
        pass
        #status, msg = logcat_initialize(devicesId)
    elif log_status == "STOP":
        pass
        #status, msg = logcat_stop(devicesId) 
        
    """
    #if yamlData["testcase_config"][tst].has_key("tempDevicesId"):
    if "tempDevicesId" in yamlData["testcase_config"][tst].keys():
        devicesId.extend(yamlData["testcase_config"][tst]["tempDevicesId"])
        devicesNames.extend(yamlData["testcase_config"][tst]["tempDevicesName"])

    for devices in devicesNames:
        device_index = devicesNames.index(devices)
        devId = devicesId[device_index]

        if int(log_type) == 0:
            if log_status == "START":
                print("Starting the logs.......")
                status, msg = delete_log(devices, devId)
                status, msg = start_log(devices, devId)
            elif log_status == "STOP":
                print("Stopping the logs.......")
                status, msg = stop_log(devices, devId, gc.IMAGE_FOLDER)

            else:
                pass
            
        elif int(log_type) == 1:
            if gc.CURRENT_TC_COUNT == 1 and log_status == "START":
                print("Starting the logs.......")
                status, msg = delete_log(devices, devId)
                status, msg = start_log(devices, devId)
                        
            elif log_status == "RESTART" and gc.CURRENT_TC_COUNT != yamlData['testCase'][0][tst]:
                print("Test case Failed....Restarting Logs!!!!!!!!!!!!!!!!!")
                status, msg = stop_log(devices, devId, "{0}/../".format(gc.IMAGE_FOLDER))
                status, msg = start_log(devices, devId)

            elif log_status == "STOP" and gc.CURRENT_TC_COUNT == yamlData['testCase'][0][tst]:
                print("Stopping the logs.......")
                status, msg = stop_log(devices, devId, "{0}/../".format(gc.IMAGE_FOLDER))
            
            else:
                pass

     """