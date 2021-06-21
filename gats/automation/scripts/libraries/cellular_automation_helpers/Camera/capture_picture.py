import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
import os
import linecache
import warnings
warnings.filterwarnings("ignore")

# Redirecting logs
log = logging.getLogger(__name__)



class perf_cam_cap:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_capture_pic(self):
        log.debug("==Entering into rear camera block==")
        (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} logcat -c")
        if not status:
            return False, "Not executed"

        # Press HomeScreen
        home_cmd = f"adb -s {self.Data['serialId']} shell am start -W -c android.intent.category.HOME -a android.intent.action.MAIN"
        (output, error, status) = cf.execute_commands(home_cmd)

        if not status:
            return False, f'{error.decode("utf-8")}'

        time.sleep(2)
        # Opening Camera..
        status, msg = adb.open_camera_capture_image(deviceId=self.Data['serialId'])

        if not status:
            return False, msg
        time.sleep(1)

        time.sleep(5)
        log.info("Browse the picture")
        browse = f"adb -s {self.Data['serialId']} shell ls -t /storage/emulated/0/DCIM/Camera | head -1 > {gc.IMAGE_FOLDER}/camera_file.txt"
        (output, error, status) = cf.execute_commands(browse)

        if not status:
            return False, f"{error}"

        log.debug("Browse the picture ==> {0}".format(browse))

        camera = open(f"{gc.IMAGE_FOLDER}/camera_file.txt", "r+")
        image = camera.readline()
        image = image[:-1]
        print(image)
        log.info("File name stored as \"{0}\" ".format(image))
        time.sleep(5)
        log.info("Closing Camera..")

        # Closing Camera app
        cam_cmd = f"adb -s {self.Data['serialId']} shell am force-stop com.google.android.GoogleCamera"
        (output, error, status) = cf.execute_commands(cam_cmd)
        log.debug("Closing Camera ==> {0}".format(cam_cmd))

        time.sleep(5)

        # Browse and display the picture
        log.info("Browse the file {0}".format(image))
        status_cmd = f"adb -s {self.Data['serialId']} shell ls -t /storage/emulated/0/DCIM/Camera/ | head -1 > {gc.IMAGE_FOLDER}/camera_file.txt"
        (output, error, status) = cf.execute_commands(status_cmd)
        os.system(f"adb -s {self.Data['serialId']} shell ls /storage/emulated/0/DCIM/Camera/{image} > /dev/null 2>&1 && echo \"File is exists\" || echo \"File isn't exists\" ")
        log.debug("Browse the file =====> {0}".format(status_cmd))

        # Browse file Delete file
        if (linecache.getline(f"{self.Data['serialId']}/camera_file.txt", 1)) == image:
            log.info("File isn't exist..Please Capture again !!")

        else:
            log.info("Display the latest picture {0}".format(image))
            view_cmd = f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.VIEW -d file:///storage/emulated/0/DCIM/Camera/{image} -t image/*"
            (output, error, status) = cf.execute_commands(view_cmd)
            log.debug("Display the latest picture{0}".format(view_cmd))

            time.sleep(5)
            (output, error, status) = cf.execute_commands(home_cmd)

            # Delete the picture
            log.info("Deleted the latest picture {0}".format(image))
            del_cmd = f"adb -s {self.Data['serialId']} shell rm /storage/emulated/0/DCIM/Camera/{image} "
            (output, error, status) = cf.execute_commands(del_cmd)
            log.debug("Deleted the latest picture {0}".format(image))

            time.sleep(5)

            # Valudation of deleted picture
            log.info("Validation of deleted picture {0}".format(image))
            os.system(f"adb -s {self.Data['serialId']} shell ls /storage/emulated/0/DCIM/Camera/{image} > /dev/null 2>&1 && echo \"File is exists\" || echo \"File isn't exists\" ")
            time.sleep(2)
        log.info("Test case executed successfully")
        return True, "Rear Camera executed"


def capture_picture(tst, yamlData):
    call_obj = perf_cam_cap(tst, yamlData)
    status, msg = call_obj.execute_capture_pic()
    return status, "Rear Camera executed"
