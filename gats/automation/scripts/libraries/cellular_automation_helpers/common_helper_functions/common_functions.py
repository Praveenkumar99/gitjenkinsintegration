#Builtin module
import re
import os
import time
import logging
import subprocess
import datetime
import automation_helpers.globalconstants as gc

Log = logging.getLogger(__name__)


def test_mode_air(status, Data):
    """To Turn ON Airplane Mode using adb
    Args:
        status: Mentions airplane to made ON/OFF
    """
    Log.info("Turning Airplane Mode {}..........".format(status))
    Log.info("==========>{}<=========".format(gc.IMAGE_FOLDER))
    airplane_on = "settings put global airplane_mode_on 1\n"
    airplane_off = "settings put global airplane_mode_on 0\n"
    am_command = "su 0 am broadcast -a android.intent.action.AIRPLANE_MODE\n"
    _proc = subprocess.Popen("adb -s {0} shell".format(Data["serialId"]),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    if status == 'ON':
        _proc.stdin.write(airplane_on.encode('utf-8'))
    else:
        _proc.stdin.write(airplane_off.encode('utf-8'))
    _proc.stdin.write(am_command.encode('utf-8'))
    _stdout, _stderr = _proc.communicate()
    Log.info(print(_proc.returncode))
    time.sleep(5)
    if _proc.returncode == 0:
        return True, 'Successfully Turned on Airplane mode: {}'.format(_stdout)
    return False, 'Failed to Turn on Airplane Mode: {}'.format(_stderr)

def check_attach(Data):
    """Checking the device attach status
    Args:
        Data:yaml data read from user input for execution
    """
    Log.info("Checking Wether DUT Attach to the Network or Not..................")
    print(Data["serialId"], gc.IMAGE_FOLDER)
    (output, error, status) = execute_commands("adb -s {0} shell ifconfig > {1}/check.txt".format(Data["serialId"], gc.IMAGE_FOLDER))
    if status == True :
        with open("{0}/check.txt".format(gc.IMAGE_FOLDER), "r") as f :
            for l in f.readlines():
                if "255.255.255.0" in l:
                    res = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",l)
                    print(res)
                    print("DUT is attachetd to the ip :",res[0])
                    if res[0]:
                        Log.info("=====> UE Attached <==== ")
                        print("=====> UE Attached <==== ")
                        Log.info("====> IP Address : {} <==== ".format(res[0]))
                    return True, "Attach is successfull"
            else :
                f.close()
                return False, "Attach is not successfull"
    else :
        return False, error

def execute_commands(cmd) :
    proc = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    (output,error) = proc.communicate()
    error = "return code --- >"+str(proc.returncode)+"\nerror --- >"+str(error)
    if proc.returncode == 0:
        return output,error, True
    else :
        return output,error,False


def get_input_path(file_name, module):
    """
    Gives the input path for the files
    :param file_name: ``file name``
    :author: Sayyuf Shaik
    :return:
    """
    print("******************************************************")
    print("IMAGE FOLDER IS ", gc.IMAGE_FOLDER)
    print("******************************************************")
    return os.path.join(gc.IMAGE_FOLDER, '..', '..', 'inputs', module, file_name)


def comp_id(deviceId):
    cmd = "adb devices > {0}/device_name.txt".format(gc.IMAGE_FOLDER)
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    (output, error) = proc.communicate()
    if proc.returncode == 0:
        status = []
        noOfDevices = 1
        with open("{0}/device_name.txt".format(gc.IMAGE_FOLDER)) as deviceFile:
            for line in deviceFile:
                for deviceNo in deviceId:
                    if deviceNo in line and "device" in line:
                        status.append(True)
                        noOfDevices += 1
            (output, error, exec_status) = execute_commands("rm {0}/device_name.txt".format(gc.IMAGE_FOLDER))
            if all(status):
                return True, "Devices are connected", noOfDevices
            return False, "Device are not connected", noOfDevices
    else:
        return False, error, 0

def xml_file_parser(searchString, deviceId):
    Log.info("==dumping UI==")
    (output, error, status) = execute_commands(
        "adb -s {0} shell uiautomator dump".format(deviceId))

    if not status:
        return False, []

    Log.info("=Downloading the file from device=")
    (output, error, status) = execute_commands(
        "adb -s {0} pull sdcard/window_dump.xml {1}".format(deviceId,
                                                            gc.IMAGE_FOLDER))
    if not status:
        return False, []

    with open("{0}/window_dump.xml".format(gc.IMAGE_FOLDER), "r") as fd:
        s = ""
        d = fd.read()

        if searchString == "plane":
            x = re.search('\w+plane', d)
            if x:
                searchString = x.group()+ " mode"
        Log.info(searchString)
        i = d.find(f'text="{searchString}"')

        if i == -1:
            s = f'content-desc="{searchString}'
            i = d.find(s)
            if i == -1:
                return False, []
        while d[i] != '>':
            i += 1
        else:
            i -= 3
            while d[i] != '=':
                i -= 1
                s += d[i]
    s = s[::-1]
    temp = re.findall(r'\d+', s)
    param = list(map(int, temp))
    print(param)
    if deviceId == "LGH8608e7508fe":
        res = param[:2]
    else:
        res = param[2:]
    return True, res

def xml_file_parser1(searchString, deviceId):
    Log.info("==dumping UI==")
    (output, error, status) = execute_commands("adb -s {0} shell uiautomator dump".format(deviceId))
    if not status:
        return False, []
    Log.info("=Downloading the file from device=")
    (output, error, status) = execute_commands("adb -s {0} pull sdcard/window_dump.xml {1}".format(deviceId, gc.IMAGE_FOLDER))
    if not status:
        return False, []
    with open("{0}/window_dump.xml".format(gc.IMAGE_FOLDER), "r") as fd:
        s = ""
        e = fd.read()
        a = ""
        i = e.find(f'text="{searchString}"')
        
        while e[i] != '&':
            s += e[i]
            i += 1
        else:
            while e[i] != ':':
                i = i - 1
                a += e[i]
        a = a[-2::-1]
        return a

def fetch_call_state(mobileNumber):
    data1 = re.compile(r'(mCallState=([0-2]))')
    data2 = re.compile(r'(mCallIncomingNumber=(\+[0-9]{12}))')
    mCallState = []
    status = True
    with open("{0}/dump.txt".format(gc.IMAGE_FOLDER), "r") as fd:
        for line in fd.readlines():
            for match in re.findall(data1, line):
                callState = int(match[1])
                mCallState.append(str(callState))
            for match in re.findall(data2, line):
                if match[1][3:] == str(mobileNumber):
                    status = True
    (output, error, status) = execute_commands("rm {0}/dump.txt".format(gc.IMAGE_FOLDER))
    mCallState = [int(items) for items in mCallState]
    return status, max(mCallState)


def concurrency_call(sec, deviceId, mobileNumber):
    counter = sec
    start = time.time()
    while True:
        # it won't be blocked
        time.sleep(0.1)
        os.system(
            "adb -s {0} shell dumpsys telephony.registry | grep \"mCallState\|mCallIncomingNumber\" > {1}/dump.txt".format(
                deviceId, gc.IMAGE_FOLDER))
        status, mCallState = fetch_call_state(mobileNumber)
        if mCallState == 0:
            return False, "Concurrency of calling is failed !!"
        # When 1 sec or more has elapsed...
        if time.time() - start > 1:
            start = time.time()
            counter = counter - 1
            # print("%s seconds" %counter)
            # Countdown finished, ending loop
            if counter <= 0:
                break

    return True, "Concurrency calling performed sucessfully"

def disconnect_call(deviceId):
    cmd = "adb -s {0} shell dumpsys telephony.registry | grep \"mCallState\|mCallIncomingNumber\" > {1}/dump.txt".format(
        deviceId, gc.IMAGE_FOLDER)
    (output, error, status) = execute_commands(cmd)
    if fetch_call_state_1() == 1:
        (output, error, status) = execute_commands(
            f"adb -s {deviceId} shell input keyevent KEYCODE_ENDCALL")
    elif fetch_call_state_1() == 2:
        (output, error, status) = execute_commands(
            f"adb -s {deviceId} shell input keyevent KEYCODE_ENDCALL")
    else:
        pass

def getDeviceTemprature():
    with open("{0}/temp.txt".format(gc.IMAGE_FOLDER), "r") as fd:
        temp = re.findall(r'\d+', fd.read())
        res = list(map(int, temp))
        return res[0] / 10

def toggle_airplane_mode(deviceId):
    Log.info("Toggling")
    cmd = "adb -s {0} shell am start -a android.settings.WIRELESS_SETTINGS".format(deviceId)
    (output, error, status) = execute_commands(cmd)
    time.sleep(3)
    status, coordinate = xml_file_parser("plane", deviceId)
    cmd = "adb -s {0} shell input tap {1} {2}".format(deviceId, str(coordinate[0]), str(coordinate[1]))
    execute_commands(cmd)
    time.sleep(5)
    execute_commands(cmd)
    os.system("adb -s {0} shell settings get global airplane_mode_on > {1}/status.txt".format(deviceId,gc.IMAGE_FOLDER))
    fd = open("{0}/status.txt".format(gc.IMAGE_FOLDER), "r+")
    status = fd.readline()
    return status