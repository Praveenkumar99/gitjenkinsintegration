# Volte call hold/Unhold

import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
import cellular_automation_helpers.common_helper_functions.ui_automator as ui
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class OnHold:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def hold_from_mo_side(self):
        log.info("==Making a call from MO to MT to put call on Hold to Unhold==")

        # Triggering the Call from Device MO
        status, msg = adb.trigger_volte_call(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callB_no"])

        if not status:
            return False, msg

        # fetching the call state of Devices MT
        status, mCallState = adb.check_call_state(
            deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0],
            phoneNumber=self.Data['testcase_config'][self.tst]["callA_no"]
        )

        if not status:
            return False, mCallState

        # Receiving the Call in Devices MO
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "Call not received in devices B"

        log.info("Receiving call in device B")
        status, msg = adb.accept_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg

        log.info("Call answered successfully @ MT side")
        
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['Call_duration']
        #timeout = time.time() + 60
        
        i = 0
        # Performing the hold and unhold
        while True:
            if time.time() > timeout:
                break
            else:
                for i in range(1, 65):
                    if time.time() > timeout:
                        break
                        
                    status, msg = cf.concurrency_call(  
                        1,
                        self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
                        self.Data['testcase_config'][self.tst]["callA_no"])
                    
                    if not status:
                        return False, "Call in between disconnected"
                    
                    # performing Hold
                    log.info(f"Performing Hold for {i} time")
                    status, msg = ui.putCallOnHold(self.Data['serialId'])
                    
                    if not status:
                        return False, msg
                    
                    time.sleep(30)
                    
                    # performing Un-Hold
                    log.info(f"Performing Un-Hold for {i} time")
                    status, msg = ui.putCallOnHold(self.Data['serialId'])
                    
                    if not status:
                        return False, msg
                    
                    time.sleep(29)
                    
        # Disconnecting the Call
        log.info("Terminating call @ MO side")
        status, msg = adb.terminate_call(deviceId=self.Data['serialId'])
        if not status:
            return False, msg

        return True, "Hold Performed Successful from MO Side"

    def hold_from_mt_side(self):
        log.info("==Making a call from MT to MO to put call on Hold to Unhold==")
        
        # Triggering the Call from Device MT
        status, msg = adb.trigger_volte_call(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callB_no"])

        if not status:
            return False, msg

        # fetching the call state of Devices MO
        status, mCallState = adb.check_call_state(
            deviceId=self.Data['serialId'],
            phoneNumber=self.Data['testcase_config'][self.tst]["callB_no"]
        )

        if not status:
            return False, mCallState

        # Receiving the Call in Devices MO
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "Call not received in devices MO"

        log.info("Receiving call in device MO")
        status, msg = adb.accept_call(deviceId=self.Data['serialId'])

        if not status:
            return False, msg

        log.info("Call attended successfully @ MO side")
        
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['Call_duration']
        #timeout = time.time() + 60
        
        i = 0
        # Performing the hold and unhold
        while True:
            if time.time() > timeout:
                break
            else:
                for i in range(1, 65):
                    if time.time() > timeout:
                        break
                    status, msg = cf.concurrency_call(
                        
                        1,
                        self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
                        self.Data['testcase_config'][self.tst]["callA_no"])
                    
                    if not status:
                        return False, "Call in between disconnected"
                    
                    # performing Hold
                    log.info(f"Performing Hold for {i} time")
                    status, msg = ui.putCallOnHold(
                        self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
                    
                    if not status:
                        return False, msg
                    
                    time.sleep(30)
                    # performing Un-Hold
                    log.info(f"Performing Un-Hold for {i} time")
                    status, msg = ui.putCallOnHold(
                        self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
                    
                    if not status:
                        return False, msg
                    
                    time.sleep(29)
                    
        # Disconnecting the Call
        log.info("Terminating call @ MT side")
        status, msg = adb.terminate_call(
            self.Data['testcase_config'][self.tst]['tempDevicesId'][0])
        if not status:
            return False, msg

        return True, "Hold Performed Successful from MO Side"
    
    def execute_call(self):
        # Peroforming Hold-Unhold from MO
        status, msg = self.hold_from_mo_side()
        if not status:
            return False, msg
        
        # Peroforming Hold-Unhold from MT
        status, msg = self.hold_from_mo_side()
        if not status:
            return False, msg
        
        return True, f"{__name__} Passsed Successfully."

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

def perform_hold(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = OnHold(tst, yamlData)
        status, msg = call_obj.execute_call()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg