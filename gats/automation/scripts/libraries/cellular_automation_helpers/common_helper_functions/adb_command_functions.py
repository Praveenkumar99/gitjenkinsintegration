import cellular_automation_helpers.common_helper_functions.common_functions as cf
import automation_helpers.globalconstants as gc
import time
import logging
import re
import os
from enum import Enum
from uiautomator import Device

log = logging.getLogger(__name__)


class CallStates(Enum):
    IDLE_CALL = 0
    INCOMING_CALL = 1
    CONNECTED_CALL = 2


def rebootDevice(deviceId):
    """
        function name  : putCallOnHold
        description    : this function is a used to fetch the call state.
        return         : return boolean, string(mCallState)
    """
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} reboot")

    if not status:
        return False, f"Rebooting the devices failed due to {error}"

    log.info("Devices Reboot started successfully")
    return True, "Devices Reboot started successfully"


def launchApplication(deviceId, packageName, activityName):
    """
        function name  : putCallOnHold
        description    : this function is a used to fetch the call state.
        return         : return boolean, string(mCallState)
    """
    cmd = f'adb -s {deviceId} shell am start -n {packageName}/{activityName}'
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, "launching application"
    return True, "Game Launched"


def check_battery_level(deviceId):
    cmd = f'adb -s {deviceId} shell dumpsys battery | grep level'
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"Checking BATTERY level failed due to {error}"

    return True, f'Battery level is {output.decode("utf-8")}'

def memory_utiliztion(deviceId):
    cmd = f'adb -s {deviceId} shell vmstat'
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"Checking MEMORY utilization failed failed due to {error}"

    return True, f'Memory Utilization {output.decode("utf-8")}'


def cpu_usage(deviceId):
    cmd = f'adb -s {deviceId} shell top -m 10'
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"Checking CPU usage failed failed due to {error}"

    return True, f'CPU usage {output.decode("utf-8")}'

def stream_video(deviceId, exec_status, http_link):
    """
        function name  : Streaming Video, stream youtube video.
        return         : return boolean, status message
    """

    if exec_status == "START":
        start_video_command = str("adb -s {0} shell am start -a android.intent.action.VIEW -d {1} ".format(deviceId, http_link))
        (output, error, status) = cf.execute_commands(start_video_command)
        if not status:
            return False, "Error while opening Youtube"
        return True, "Youtube video is streaming"
    
    elif exec_status == "STOP":
        stop_video_command = str("adb -s {0} shell am force-stop com.google.android.youtube".format(deviceId))
        (output, error, status) = cf.execute_commands(stop_video_command)
        if not status:
            return False, "Error while closing Youtube"
        return True, "Youtube video is closed"
    
    return True, ""


def imsRegistrationValidator(deviceId):
    """
        function name  : imsRegistrationValidator
        description    : this function is a used to fetch the ims state.
        return         : return boolean, string(mCallState)
    """
    log.info("Checking the ims registration")
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} logcat -d | grep  'RcsEngine.updateRcsImsState:' >> {gc.IMAGE_FOLDER}/ims.txt")

    if not status:
        return False, str(error)

    # ims status in last line so fetching the info
    with open(f"{gc.IMAGE_FOLDER}/ims.txt", 'r') as fd:
        data = fd.readlines()
        for lastline in data:
            pass
    print(lastline)
    if 'REGISTRATION_SUCCESSFUL' not in lastline:
        os.remove(f"{gc.IMAGE_FOLDER}/ims.txt")

        return False, "Ims registration failed"

    os.remove(f"{gc.IMAGE_FOLDER}/ims.txt")

    return True, "Ims registration Done"

def putCallOnHold(deviceId):
    """
        function name  : putCallOnHold
        description    : this function is a used to fetch the call state.
        return         : return boolean, string(mCallState)
    """
    
    try:
        d = Device(deviceId)
        if d.screen != "on":
            d.screen.on()
        status = d(text="Hold").click()
    
    except Exception as e:
        return False, f"Execption occured {str(e)}"
    if not status:
        return False, "Tapping on Hold failed"
    
    return True, "Hold performed successful"

def swap_call(deviceId):
    """
        function name  : putCallOnHold
        description    : this function is a used to fetch the call state.
        return         : return boolean, string(mCallState)
    """
    d = Device(deviceId)
    status = d(text="Swap").click()
    if not status:
        return False, "Tapping on Hold failed"
    
    return True, "Hold performed successful"

def trigger_volte_call(deviceId, phoneNumber):
    """
        function name  : trigger_volte_call
        description    : this function is a used perform the volte call
        return         : return boolean, string
    """
    # Adb command for triggering Volte call
    cmd = f"adb -s {deviceId} shell am start -a android.intent.action.CALL -d tel:{phoneNumber}"
    log.info(f"Calling from device {deviceId} ===> {cmd}")
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"Triggering call failed due to {error}"
    time.sleep(10)
    return True, "Call Performed Successfully"


def trigger_vt_call(deviceId, phoneNumber):
    """
        function name  : trigger_vt_call
        description    : this function is a used perform the VT call
        return         : return boolean, string
    """
    # Adb command for triggering VT call
    cmd = f"adb -s {deviceId} shell am start -a android.intent.action.CALL -d tel:{phoneNumber} " \
          f"--ei android.telecom.extra.START_CALL_WITH_VIDEO_STATE 3"

    log.info(f"VT Calling from device {deviceId} ===> {cmd}")
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"Triggering VT call failed due to {error}"
    time.sleep(10)
    return True, "VT Call Performed Successfully"


def check_call_state(deviceId, phoneNumber):
    """
        function name  : fetch_call_state
        description    : this function is a used to fetch the call state.
        return         : return boolean, string(mCallState)
    """
    # adb command for fetching mCallState
    cmd = f"adb -s {deviceId} shell dumpsys telephony.registry | grep \"mCallState\|mCallIncomingNumber\"" \
          f" > {gc.IMAGE_FOLDER}/dump.txt"
    log.debug("Checking device {1} ===> {0}".format(cmd, deviceId))
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"Executing the {cmd} failed, due to {error}"

    # fetching the mCallState value from dump.txt file
    status, mCallState = cf.fetch_call_state(phoneNumber)

    if not status:
        return False, f"fetching the call state of {deviceId} failed"

    log.info(f"Call state fetched successfully and call state is {mCallState}")
    return True, mCallState


def accept_call(deviceId):
    """
        function name  :  receive_call
        description    : This function used to pick the call.
        return         : return boolean, string(mCallState)
    """
    # adb command for accept call
    call_attend = f"adb -s {deviceId} shell input keyevent KEYCODE_CALL"
    log.debug(f"Receiving call in device {deviceId} ===> {call_attend}")
    (output, error, status) = cf.execute_commands(call_attend)

    if not status:
        return False, f"Receiving Call failed due to {error}"

    log.info("Call received Successfully")
    return True, "Call received Successfully"


def terminate_call(deviceId):
    """
        function name  :  terminating the call
        description    : This function used to disconnect the call.
        return         : return boolean, string(mCallState)
    """
    # adb command for disconnect the call
    disconnect_cmd = f"adb -s {deviceId} shell input keyevent KEYCODE_ENDCALL"
    log.debug("Terminating call in device {1} ===> {0}".format(disconnect_cmd, deviceId))
    (output, error, status) = cf.execute_commands(disconnect_cmd)

    if not status:
        return False, f"Terminating the call failed due to {error}"

    log.info("Call terminated Successfully")
    return True, "Call terminated Successfully"


def checking_call_state():
    """
       function name  :  checking_call_state
       description    : This function used check the call state before the disconnect call.
       return         : return integer
    """
    # Parsing for mCallState from dump.txt
    data1 = re.compile(r'(mCallState=([0-2]))')
    mCallState = []
    status = False
    for line in open("{0}/dump.txt".format(gc.IMAGE_FOLDER), "r"):
        for match in re.findall(data1, line):
            callState = int(match[1])
            mCallState.append(str(callState))
    mCallState = [int(items) for items in mCallState]
    return max(mCallState)


def lock_screen(deviceId):
    """
           function name  :  lock_screen.
           description    : This function used for lock the screen.
           return         : return
    """
    # Locking the phone
    (output, error, status) = cf.execute_commands(f"adb -s {deviceId} shell input keyevent 26")
    log.debug("Locked the Screen")
    if not status:
        return False, "Locking Screen failed MO side"

    return True, "Successfully locked the screenshot."


def tap_command(deviceId, x, y):
    """
           function name  :  graceful_disconnection used for hard disconnect call.
           description    : This function used for hard disconnect call whenever failure occurs.
           return         : return
    """
    # adb command for Tap
    (output, error, status) = cf.execute_commands(
        f"adb -s {deviceId} shell input tap {x} {y}")

    time.sleep(5)

    if not status:
        return False, f"Tapping on {x}, {y} failed due to {error} in device {deviceId}"

    return True, "Tapped Successful"


def graceful_disconnection(deviceId):
    """
       function name  :  graceful_disconnection used for hard disconnect call.
       description    : This function used for hard disconnect call whenever failure occurs.
       return         : return
    """
    # Checking the Call state
    cmd = "adb -s {0} shell dumpsys telephony.registry | grep \"mCallState\|mCallIncomingNumber\" > " \
          "{1}/dump.txt".format(deviceId, gc.IMAGE_FOLDER)

    log.debug("Checking device {1} ===> {0}".format(cmd, deviceId))
    cf.execute_commands(cmd)

    # Validating the call state and Terminating call for call state > 0
    if checking_call_state() > CallStates.IDLE_CALL.value:
        terminate_call(deviceId)

def perform_a2b_call(deviceId1, deviceId2, callA, callB):
    """
       function name  :  perform_a2b_call
       description    : This function perform call from devices A to B , B Accept the call.
       return         : return
    """
    # Triggering the Call from Device A
    status, msg = trigger_volte_call(
        deviceId=deviceId1,
        phoneNumber=callB)

    if not status:
        return False, msg

    # fetching the call state of Devices B
    status, mCallState = check_call_state(
        deviceId=deviceId2,
        phoneNumber=callA
    )

    if not status:
        return False, mCallState

    # Receiving the Call in Devices B
    if mCallState != CallStates.INCOMING_CALL.value:
        return False, "Call not received in devices B"

    log.info("Receiving call in device B")
    status, msg = accept_call(deviceId=deviceId2)

    if not status:
        return False, msg

    return True, msg


def perform_a2b_vt_call(deviceId1, deviceId2, callA, callB):
    """
       function name  :  perform_a2b_vt_call
       description    : This function perform VT call from devices A to B , B Accept the VTcall.
       return         : return boolean, string
    """
    # Triggering the Call from Device A
    status, msg = trigger_vt_call(
        deviceId=deviceId1,
        phoneNumber=callB)

    if not status:
        return False, msg

    # fetching the call state of Devices B
    status, mCallState = check_call_state(
        deviceId=deviceId2,
        phoneNumber=callA
    )

    if not status:
        return False, mCallState

    # Receiving the Call in Devices B
    if mCallState != CallStates.INCOMING_CALL.value:
        return False, "Call not received in devices B"

    log.info("Receiving call in device B")
    status, msg = accept_call(deviceId=deviceId2)

    if not status:
        return False, msg

    return True, msg

def play_audio(deviceId, audio_file_path, fileFormate):
    """
       function name  :  play_audio
       description    : This function used to play audio file
       return         : return
    """
    cmd = f"adb -s {deviceId} shell am start -a android.intent.action.VIEW -d {audio_file_path} -t {fileFormate}"
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"playing audio command failed due to {error}"
    time.sleep(10)

    return True, f"This {audio_file_path} audio file played successfully"

def play_video(deviceId, video_file_path, fileFormate):
    """
       function name  :  play_video
       description    : This function perform VT call from devices A to B , B Accept the VTcall.
       return         : return boolean, string
    """
    cmd = f"adb -s {deviceId} shell am start -a android.intent.action.VIEW -d {video_file_path} -t {fileFormate}"
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"playing audio command failed due to {error}"
    time.sleep(10)

    return True, f"This {video_file_path} audio file played successfully"

def stop_media(deviceId):
    """
       function name  :  stop_media
       description    : This function used to stop the media file playing
       return         : return boolean, string
    """
    log.info("Stopping Media File")
    cmd = f"adb -s {deviceId} shell input keyevent 3"
    (output, error, status) = cf.execute_commands(cmd)

    if not status:
        return False, f"Stopping media command failed due to {error}"

    time.sleep(1)
    return True, "Media Stopped Successfully"

def open_camera_capture_image(deviceId):
    cam_cmd = f"adb -s {deviceId} shell am start -a android.media.action.IMAGE_CAPTURE"
    (output, error, status) = cf.execute_commands(cam_cmd)
    if not status:
        return False, "Opening camera failed"

    log.debug("Opening Camera ==> {0}".format(cam_cmd))

    time.sleep(1)

    log.info("Captured picture")
    img_cmd = f"adb -s {deviceId} shell input keyevent 25"
    (output, error, status) = cf.execute_commands(img_cmd)

    if not status:
        return False, "Capturing command failed"

    log.debug("Captured picture ==> {0}".format(img_cmd))
    return True, "Picture Captured Successfully"

def check_device_heat(deviceId):
    (output, error, status) = cf.execute_commands(
        f'adb -s {deviceId} shell dumpsys battery | '
        f'grep "temperature:" >> {gc.IMAGE_FOLDER}/temp.txt')

    if not status:
        return False, "temperature measuring command Failed in A side"

    temp1 = cf.getDeviceTemprature(gc.IMAGE_FOLDER)

    return True, temp1

def send_sms(deviceId, phoneNumber):
    (output, error, status) = cf.execute_commands(
        f"adb -s {deviceId} shell am start -a android.intent.action.SENDTO -d "
        f"sms:{phoneNumber} --es "
        f"sms_body HELLO --ez exit_on_sent true")

    if not status:
        return False, "Opening SMS App failed"

    (output, error, status) = cf.execute_commands(
        f"adb -s {deviceId} shell input keyevent 22")

    if not status:
        return False, "Clicking on Next 1 failed"

    (output, error, status) = cf.execute_commands(
        f"adb -s {deviceId} shell input keyevent 22")

    if not status:
        return False, "Clicking on Next 2 failed"

    (output, error, status) = cf.execute_commands(
        f"adb -s {deviceId} shell input keyevent 66")

    if not status:
        return False, "Clicking on Send failed"

    return True, "Success"

def swipe_up(deviceId):
    """
       function name  :  downgrade_call
       description    : This function used for downgarde VT call.
       return         : return
    """
    d = Device(deviceId)
    d(resourceId="com.google.android.dialer:id/incoming_call_puck_bg").drag.to(text="Answer as voice call", steps=2)

    return True, "Call Successfully Downgraded"

def upgrade_call(deviceId):
    """
       function name  :  upgrade_call
       description    : This function used for upgarde the volte call.
       return         : return boolean, string
    """
    # adb command for downgrade the call
    log.info("Dumping the Coordinates for Video call, Because to perform Upgard the call")

    status, coordinates = cf.xml_file_parser("Video call", deviceId)

    if not status and coordinates == []:
        return False, "Fetching the coordinates for Video call failed"

    log.info("Tapping on Video call")
    status, msg = tap_command(deviceId, coordinates[0], coordinates[1])

    if not status:
        return False, "Tapping on Video call failed"

    return True, "Call Successfully Upgraded"

def downgrade_call(deviceId):
    """
       function name  :  downgrade_call
       description    : This function used for downgarde VT call.
       return         : return
    """
    # adb command for downgrade the call
    # log.info("Dumping the Coordinates for Audio call, Because to perform downgard the call")

    # status, coordinates = cf.xml_file_parser("Audio", deviceId)
    # print(coordinates)

    # if not status and coordinates == []:
    #     return False, "Fetching the coordinates for Audio call failed"

    
    # return True, coordinates
    # log.info("Tapping on Audio call")
    # status, msg = tap_command(deviceId, coordinates[0], coordinates[1])

    # if not status:
    #     return False, "Tapping on Audio call failed"

    from uiautomator import Device

    d = Device(deviceId)
    d(resourceId="com.google.android.dialer:id/videocall_downgrade_call_button").click()

    return True, "Call Successfully Downgraded"
