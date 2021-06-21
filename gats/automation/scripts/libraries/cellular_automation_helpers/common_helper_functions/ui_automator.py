import cellular_automation_helpers.common_helper_functions.common_functions as cf
import automation_helpers.globalconstants as gc
import time
import logging
import re
from enum import Enum
from uiautomator import Device

def putCallOnHold(deviceId):
    """
        function name  : putCallOnHold
        description    : this function is a used to put call on hold
        return         : return boolean, string(mCallState)
    """
    
    
    d = Device(deviceId)
    if d.screen != "on":
        d.screen.on()
    if d(text="Hold").exists:
        status = d(text="Hold").click()
    else:
        status = d.click(50, 100)
        if not d(textStartsWith="Hold").exists:
            return False, "Put call on hold failed"
        status = d(textStartsWith="Hold").click()
    return status, "Hold performed successful"

def swap_call(deviceId):
    """
        function name  : putCallOnHold
        description    : this function is a used to swap calls
        return         : return boolean, string(mCallState)
    """

    d = Device(deviceId)
    if d.screen != "on":
        d.screen.on()
    if d(textStartsWith="Swap").exists:
        status = d(textStartsWith="Swap").click()
    else:
        status = d.click(50, 100)
        if not d(textStartsWith="Swap").exists:
            return False, "Put call on Swap failed"
        status = d(textStartsWith="Swap").click()
    return status, "Swap performed successful"

def merge_calls(deviceId):
    """
       function name  :  Merge calls
       description    : This function is used to merge calls.
       return         : return boolean, string
    """
    # Using UI automater
    d = Device(deviceId)
    if d.screen != "on":
        d.screen.on()
    if d(textStartsWith="Merge").exists:
        status = d(textStartsWith="Merge").click()
    else:
        status = d.click(50, 100)
        if not d(textStartsWith="Merge").exists:
            return False, "Merging call failed"
        status = d(textStartsWith="Merge").click()
    return status, "Merge performed successful"

def upgrade_call(deviceId):
    """
       function name  :  upgrade_call
       description    : This function is used to upgrade the calls
       return         : return boolean, string
    """
    # Using UI automater
    d = Device(deviceId)
    if d.screen != "on":
        d.screen.on()
    if d(textStartsWith="Video").exists:
        status = d(textStartsWith="Video").click()
    else:
        status = d.click(50, 100)
        if not d(textStartsWith="Video").exists:
            return False, "Video call failed"
        status = d(textStartsWith="Video").click()

    return status, "upgrade_call performed successful"
    # try:
    #     d = Device(deviceId)
    #     status = d(textStartsWith="Video").click()
    # except Exception as e:
    #     return False, f"Execption occured {str(e)}"
    
    # return status, "Merge performed successfully"

def downgrade_call(deviceId):
    """
       function name  :  downgrade_call
       description    : This function used for downgarde VT call.
       return         : return
    """
    d = Device(deviceId)
    if d.screen != "on":
        d.screen.on()
    if d(textStartsWith="Audio").exists:
        status = d(textStartsWith="Audio").click()
    else:
        status = d.click(50, 100)
        if not d(textStartsWith="Audio").exists:
            return False, "Video call failed"
        status = d(textStartsWith="Audio").click()

    return status, "downgrade_call performed successful"
    # d = Device(deviceId)
    # try:
    #     status = d(textStartsWith="Audio").click()
    #     print("Hi 1")
    # except:
    #     try:
    #         status = d(textStartsWith="Audio-only").click()
    #         print("Hi 2")
    #     except:
    #         return False, "Downgrading Call failed"
    # print("hi 3")
    # return status, "Call Successfully Downgraded"

def acceptVT_call(deviceId):
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

    

    try:
        d = Device(deviceId)
        status = d(resourceId="com.google.android.dialer:id/incoming_call_puck_bg").drag.to(text="Answer as voice call", steps=2)
    except:
        try:
            status = d(textStartsWith="ACCEPT").click()
        except:
            return False, "Accept Call failed"

    return status, "Call Successfully Downgraded"


