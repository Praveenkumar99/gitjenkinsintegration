from datetime import datetime
import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_functions as cf
import re

# Redirecting logs
log = logging.getLogger(__name__)


class Vowlan:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def closing_the_app(self):
        (output, error, status) = cf.execute_commands(
            f'adb -s {self.Data["serialId"]} shell input keyevent KEYCODE_APP_SWITCH')

        if not status:
            return False, "Opening the Recent apps failed"
        time.sleep(1)
        (output, error, status) = cf.execute_commands(f'adb -s {self.Data["serialId"]} shell input tap  555 2056')

        if not status:
            return False, "Closing all recent apps"

        return True, "All recent apps closed"

    def uidumper(self, str):

        (output, error, status) = cf.execute_commands(
            f"adb -s {self.Data['serialId']} pull $(adb  -s {self.Data['serialId']} shell uiautomator dump | "
            f"grep -oP '[^ ]+.xml') ./a.xml")

        if not status:
            return False, "Dumping the Ui failed"

        (output, error, status) = cf.execute_commands(
            f'perl -ne \'printf "%d %d\n", ($1+$3)/2, ($2+$4)/2 if /text="{str}"[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"/\' ./a.xml')

        if not status:
            return False, f"Searching for the {str} settings failed"

        x_y = re.findall(r'\d+', output.decode("utf-8"))
        x_y = list(map(int, x_y))

        return True, x_y

    def installing_apk(self):
        (output, error, status) = cf.execute_commands("wget -O ./adb-join-wifi.apk "
                                                      "https://github.com/steinwurf/adb-join-wifi/releases/download/1.0.1/adb-join-wifi.apk")
        if not status:
            return False, "Downloading the apk file failed"

        (output, error, status) = cf.execute_commands(f'adb -s {self.Data["serialId"]} install ./adb-join-wifi.apk')

        if not status:
            return False, "Installing the Apk failed"

        return True, "Apk installed Successfully"

    def test_for_heat(self):
        log.info("==Heat Stress testing On MO devices==")

        status, msg = self.installing_apk()

        if not status:
            return False, msg

        (output, error, status) = cf.execute_commands(f'adb -s {self.Data["serialId"]} shell dumpsys wifi')

        if not status:
            return False, f"Checking the Wifi state failed due to {str(error)}"

        wifi_status = output.decode("utf-8")

        (output, error, status) = cf.execute_commands(
            f'adb -s {self.Data["serialId"]} shell am start -a  "android.settings.NETWORK_OPERATOR_SETTINGS" ')

        if not status:
            return False, "Opening the NETWORK_OPERATOR_SETTINGS failed"

        status, coordinates = self.uidumper("Advanced")

        if not status:
            return False, coordinates

        (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} shell input "
                                                      f" tap {coordinates[0]} {coordinates[1]}")

        if not status:
            return False, "Taping on Advanced"

        status, coordinates = self.uidumper("Wi-Fi calling")

        if not status:
            return False, coordinates

        (output, error, status) = cf.execute_commands(
            f"adb -s {self.Data['serialId']} shell input tap {coordinates[0]} {coordinates[1]}")

        if not status:
            return False, "Tapping on Wi-Fi calling"

        status, coordinates = self.uidumper("On")

        if not status:
            return False, coordinates

        if not coordinates:
            (output, error, status) = cf.execute_commands(
                f"adb -s {self.Data['serialId']} shell input tap {coordinates[0]} {coordinates[1]}")

            if not status:
                return False, "Tapping on Wifi calling On failed"

        if wifi_status != "Wi-Fi is enabled":
            cf.execute_commands(f'adb -s {self.Data["serialId"]} shell svc wifi enable')

        if self.Data[self.tst].get('passwd') is None:
            cf.execute_commands(
                f'adb -s {self.Data["serialId"]} shell am start -n com.steinwurf.adbjoinwifi/.MainActivity '
                f'-e ssid {self.Data["testcase_config"][self.tst]["SSID"]}')
        else:
            cf.execute_commands(f'adb -s {self.Data["serialId"]} shell am start -n com.steinwurf.adbjoinwifi/.MainActivity \
                    -e ssid {self.Data[self.tst]["SSID"]} -e password_type WEP|WPA -e '
                                f'password {self.Data["testcase_config"][self.tst]["passwd"]}')

        cf.execute_commands(f'adb -s {self.Data["serialId"]} shell input keyevent 3')

        time.sleep(20)

        # make Call here
        (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} shell am start -a "
                                                      f"android.intent.action.CALL -d "
                                                      f"tel:{self.Data['testcase_config'][self.tst]['callB_no']} ")

        time.sleep(15)

        if not status:
            return False, "Not executed"

        log.info("==Picking call on MT device==")
        (output, error, status) = cf.execute_commands(
            f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][0]} shell input keyevent KEYCODE_CALL")

        if not status:
            return False, "Not executed"

        time.sleep(2)

        log.info("Disconnecting the call on MT device")

        (output, error, status) = cf.execute_commands(
            f"adb -s {self.Data['testcase_config'][self.tst]['tempDevicesId'][0]} shell input keyevent 6")

        if not status:
            return False, "Disconnecting call failed MO side"

        (output, error, status) = cf.execute_commands(f'adb -s {self.Data["serialId"]} shell svc wifi disable')

        if not status:
            return False, "Turning Off Wifi failed"

        status, msg = self.closing_the_app()

        if not status:
            return False, msg

        return True, "VoWlAN Call Performed Successfully "


def volwan_audio(tst, yamlData):
    status, msg, noOfDevices = cf.comp_id(yamlData['testcase_config'][tst]["tempDevicesId"], gc.IMAGE_FOLDER)
    if noOfDevices >= 2:
        call_obj = Vowlan(tst, yamlData)
        status, msg = call_obj.test_for_heat()
    else:
        return False, "Two Devices are needed to execute the test case, {0} device(s) connected".format(noOfDevices)
    if not status:
        cf.disconnect_call(yamlData['testcase_config'][tst]["tempDevicesId"][0])
        cf.disconnect_call(yamlData["serialId"])
    return status, msg
