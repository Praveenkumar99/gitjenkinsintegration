import re
import os
import time
import logging
import subprocess
import datetime
from datetime import datetime
from automation_helpers.YamlUtils import YamlUtils
import automation_helpers.globalconstants as gc

Log = logging.getLogger(__name__)

def execute_commands(cmd):
    proc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    (output,error) = proc.communicate()
    error = "return code --- >"+str(proc.returncode)+"\nerror --- >"+str(error)
    if proc.returncode == 0:
        return output,error, True
    else :
        return output,error,False

def delete_old_log(deviceId, logPath):
    Log.info("Deleting old pixel logs at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell rm {logPath}/*")
    time.sleep(5)
    Log.info("Deleted old pixel logs at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    return True, "Deleted old logs"


def start_pixel_logger(deviceId):
    """Staring the pixel logger Application
    """
    cmd = "adb -s {0} shell am start -n com.android.pixellogger/com.android.pixellogger.ui.main.MainActivity > logger.txt".format(deviceId)
    (output, error, status) = execute_commands(cmd)
    if status == True:
        with open("logger.txt",'r') as f:
            for l in f.readlines() :
                if "Error:" in l:
                    Log.info("error while running the pixel logger!!!")
                    f.close()
                    (output, error, status) = execute_commands("rm logger.txt")
                    return False, 'Unable to open pixel logger apk'
                else :
                    f.close()
                    (output, error, status) = execute_commands("rm logger.txt")

            (output, error, status) = execute_commands("adb -s {0} shell input tap 960 1984".format(deviceId))
    else :
        return False, 'Unable to open pixel logger apk'
    Log.info("Starting pixel logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    time.sleep(20)
    Log.info("Pixel logger is started at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    return True, 'Pixel logger has been started'

def stop_pixel_logger(deviceId):
    """Stopping the Pixel logger application
    """
    (output, error, status) = execute_commands("adb -s {0} shell am start -n com.android.pixellogger/com.android.pixellogger.ui.main.MainActivity".format(deviceId))
    Log.info("stopping pixel logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    (output, error, status) = execute_commands("adb -s {0} shell input tap 960 1984".format(deviceId))
    time.sleep(25)
    (output, error, status) = execute_commands("adb -s {0} shell am force-stop com.android.pixellogger > logger.txt".format(deviceId))

    if status == True :
        with open("logger.txt",'r') as f :
            for l in f.readlines() :
                if "Error:" in l :
                    Log.info("error while stopping the pixel logger!!!")
                    f.close()
                    (output, error, status) = execute_commands("rm logger.txt")
                    return False, 'error while stopping the pixel logger!!!'
                else :
                    f.close()
                (output, error, status) = execute_commands("rm logger.txt")
        Log.info("Pixel logger is stopped at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

        (output, error, status) = execute_commands("adb -s {0} pull /storage/emulated/0/Android/data/com.android.pixellogger/files/logs/diag_logs/ {1}/{0}".format(deviceId, gc.IMAGE_FOLDER))
        (output, error, status) = execute_commands(" adb -s {0} shell rm /storage/emulated/0/Android/data/com.android.pixellogger/files/logs/diag_logs/*".format(deviceId))
        Log.info("Logs are moved to output folder at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        return True, 'Pixel logger is stopped'
    else :
        return False, "error while stopping the pixel logger!!!"
def start_oneplus_logger(deviceId):
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell am start -a android.intent.action.VIEW -d tel:%2A%23800")
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input keyevent 18")
    if not status:
        return False, "Issue in opening log Collection"
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input keyevent 22")
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input keyevent 22")
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input keyevent 66")
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input tap 830 584")
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input tap 830 1503")
    Log.info("Starting logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

    return True, "Initiated Logs"

def stop_oneplus_logger(deviceId):
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell am start -a android.intent.action.VIEW -d tel:%2A%23800")
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input keyevent 18")
    if not status:
        return False, "Issue in opening log Collection"
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input tap 830 584")
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input tap 830 1383")
    Log.info("Stopping logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
    return True, "Stopped Log collection"

def mi_logger(deviceId, str1):
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell am start -n com.android.settings/.SubSettings")
    if not status:
        return False, ""
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input touchscreen swipe 546 2241 546 260")
    time.sleep(2)
    status, coOrdinates = xml_file_parser("Services &amp; feedback", deviceId, gc.IMAGE_FOLDER)
    cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
    (output, error, status) = execute_commands(cmd)
    (output, error, status) = execute_commands(f"adb -s {deviceId} shell input tap 967 188")

    status, coOrdinates = cf.xml_file_parser("Generate logs", deviceId, gc.IMAGE_FOLDER)
    if not status:
        return False, "Issue in generating Logs"
    cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
    (output, error, status) = execute_commands(cmd)


    if str1 == "ON":
        Log.info("Starting logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        status, coOrdinates = xml_file_parser("Generate logs", deviceId,gc.IMAGE_FOLDER)
        cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
        (output, error, status) = execute_commands(cmd)
        (output, error, status) = execute_commands(f"adb -s {deviceId} shell input tap 967 188")

    elif str1 == "OFF":
        Log.info("Stopping logger at instance {0}".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))
        status, coOrdinates = xml_file_parser("Finish and upload", deviceId, gc.IMAGE_FOLDER)
        cmd = "adb -s {0} shell input tap {1} {2} ".format(deviceId, str(coOrdinates[0]),str(coOrdinates[1]))
        (output, error, status) = execute_commands(cmd)

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

def stop_log(devName, devId):
    if devName[0:-3] == "MI_10T":
        status, msg = mi_logger(devId, "OFF")
    elif devName[0:-3] == "One_Plus":
        status, msg = stop_oneplus_logger(devId)
    elif devName[0:-3] == "GooglePixel":
        status, msg = stop_pixel_logger(devId)
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

def execute_commands(cmd):
    proc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    (output,error) = proc.communicate()
    error = "return code --- >"+str(proc.returncode)+"\nerror --- >"+str(error)
    if proc.returncode == 0:
        return output,error, True
    else :
        return output,error,False


def modem_logging(tst, log_status):
        
        gc.COMMON_YAML_DATA = YamlUtils.read_yml("yamlData", "testcase_config", gc.INPUT_IMAGE_PATH)
 
        serialId = YamlUtils.read_yml("yamlData", "serialId", gc.INPUT_IMAGE_PATH)

        deviceName = YamlUtils.read_yml("yamlData", "deviceName", gc.INPUT_IMAGE_PATH)
        gc.COMMON_YAML_DATA[tst]["tempDevicesId"].append(serialId)
        gc.COMMON_YAML_DATA[tst]["tempDevicesName"].append(deviceName)

        print("Connected Devices are ", gc.COMMON_YAML_DATA[tst]["tempDevicesName"])
        print("Serial Id is ", gc.COMMON_YAML_DATA[tst]["tempDevicesId"])
        for devices in gc.COMMON_YAML_DATA[tst]["tempDevicesName"]:
            print(devices)
            ind = gc.COMMON_YAML_DATA[tst]["tempDevicesName"]
            device_index = ind.index(devices)
            devId = gc.COMMON_YAML_DATA[tst]["tempDevicesId"][device_index]
            if log_status == "START":
                print(devices, devId)
                print("entering", gc.COMMON_YAML_DATA)
                status, msg = delete_log(devices, devId)
                status, msg = start_log(devices, devId)
                    
            elif log_status == "STOP_START":
                status, msg = stop_log(devices, devId)
                status, msg = start_log(devices, devId)

            elif log_status == "STOP":
                status, msg = stop_log(devices, devId)

        return status, msg
