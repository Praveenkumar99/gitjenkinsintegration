import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
import time

# Redirecting logs
log = logging.getLogger(__name__)


class Dou:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def trigger_volte_call(self):
        # Trigger Volte call for that duration
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

        # Receiving the VT Call in Devices MO
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "VT Call not received in devices B"

        log.info("Receiving VT call in device B")
        status, msg = adb.accept_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg

        log.info("Volte Call attended successfully @ MT side")
        status, msg = cf.concurrency_call(
            self.Data['testcase_config'][self.tst]['Call_duration'],
            self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
            self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, "Call got disconnected!!!"

        # Disconnecting the Call
        log.info("Terminating call in device B")
        status, msg = adb.terminate_call(deviceId=self.Data['serialId'])
        if not status:
            return False, msg

        return True, "VT call performed"

    def trigger_vt_call(self):
        # Trigger Vt call for that duration
        status, msg = adb.trigger_vt_call(
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

        # Receiving the VT Call in Devices MO
        if mCallState != adb.CallStates.INCOMING_CALL.value:
            return False, "VT Call not received in devices B"

        log.info("Receiving VT call in device B")
        status, msg = adb.accept_call(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])

        if not status:
            return False, msg

        log.info("VT Call attended successfully @ MT side")
        status, msg = cf.concurrency_call(
            self.Data['testcase_config'][self.tst]['Call_duration'],
            self.Data['testcase_config'][self.tst]["tempDevicesId"][0],
            self.Data['testcase_config'][self.tst]["callA_no"])

        if not status:
            return False, "Call got disconnected!!!"

        # Disconnecting the Call
        log.info("Terminating call in device B")
        status, msg = adb.terminate_call(deviceId=self.Data['serialId'])
        if not status:
            return False, msg

        return True, "VT call performed"

    def browsing(self):
        # Browsing in internet
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['browsing_duration']

        while True:
            if time.time() >= timeout:
                break
            (output, error, status) = cf.execute_commands(
                f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.VIEW -d {self.Data['testcase_config'][self.tst]['HTTP_LINK']}")

            if not status:
                return False, "Browsing in internet failed"

        return True, "Browsing performed"

    def youtube_stream(self):
        # Stream youtube
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['youtube_duration']
        status, msg = adb.stream_video(deviceId=self.Data['serialId'],
                                          http_link=self.Data['testcase_config'][self.tst]['HTTPS_LINK'],
                                          exec_status= "START")
        if not status:
                return False, msg

        while True:
            if time.time() >= timeout:
                break
            log.info("starting to play youtube video...")
            

            
        status, msg = adb.stream_video(
            self.Data['serialId'],
            self.Data['testcase_config'][self.tst]['HTTPS_LINK'], "STOP")

        if not status:
            return False, msg

        return True, "performed youtube streaming"

    def game_launch(self):
        # game launch
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['game_duration']
        log.info("starting to Game video...")
        status, msg = adb.launchApplication(self.Data['serialId'],
                                                self.Data['testcase_config'][self.tst]['game_package'],
                                                self.Data['testcase_config'][self.tst]['game_activityName'])

        if not status:
                return False, msg
        while True:
            if time.time() >= timeout:
                break

        return True, "Game Played"

    def whats_app(self):
        # game launch
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['whats_app_duration']
        status, msg = adb.launchApplication(self.Data['serialId'],
                                                "com.whatsapp",
                                                "com.whatsapp.Main")
        if not status:
            return False, msg

        while True:
            if time.time() >= timeout:
                break

            

        return True, "Whats App performed"

    def launchApp(self, activity, package, duration):
        # launch app
        timeout = time.time() + 60 * duration
        status, msg = adb.launchApplication(self.Data['serialId'],
                                                activity,
                                                package)

        if not status:
            return False, msg
        while True:
            if time.time() >= timeout:
                break
            

        return True, "App launched successfully"

    def idle(self):
        # launch app
        timeout = time.time() + 60 * self.Data['testcase_config'][self.tst]['idle_duration']

        status, msg = adb.lock_screen(
            deviceId=self.Data['serialId'])

        if not status:
            return False, msg

        while True:
            if time.time() >= timeout:
                break

        return True, "App launched successfully"

    def check_BCM(self):
        # validates Battery,
        status, msg = adb.check_battery_level(self.Data['serialId'])

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # validates CPU
        status, msg = adb.cpu_usage(self.Data['serialId'])

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # validates Memory
        status, msg = adb.cpu_usage(self.Data['serialId'])

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        return True, "performed BCM test"

    def execute(self):
        # Volte call
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Performing Volte Call')
        status, msg = self.trigger_volte_call()

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # Browsing
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Performing Browsing')
        status, msg = self.browsing()

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # Youtube
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Performing youtube')
        status, msg = self.youtube_stream()

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # Game
        status, msg = self.game_launch()

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # Whats App
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Whats App')
        status, msg = self.whats_app()

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # Vt call
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Performing VT Call')
        status, msg = self.trigger_vt_call()

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # App1
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Performing App1')
        status, msg = self.launchApp(self.Data['testcase_config'][self.tst]['app1_package'],
                                     self.Data['testcase_config'][self.tst]['app1_activity'],
                                     self.Data['testcase_config'][self.tst]['app1_duration'])

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # App2
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Performing App2')
        status, msg = self.launchApp(self.Data['testcase_config'][self.tst]['app2_package'],
                                     self.Data['testcase_config'][self.tst]['app2_activity'],
                                     self.Data['testcase_config'][self.tst]['app2_duration'])

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        # idle
        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : Performing idle')
        status, msg = self.idle()

        if not status:
            return False, msg

        status, msg = self.check_BCM()

        if not status:
            return False, msg

        log.info(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} : {msg}')

        return True, "Executed"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])
        adb.graceful_disconnection(deviceId=self.Data['testcase_config'][self.tst]['tempDevicesId'][0])


def dou_test(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"])

    # Validating the No. of Devices connected.
    if noOfDevices >= 2:
        call_obj = Dou(tst, yamlData)
        status, msg = call_obj.execute()
    else:
        return False, "One Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)

    # Validating Test case result
    if not status:
        call_obj.closeUp()

    return status, msg
