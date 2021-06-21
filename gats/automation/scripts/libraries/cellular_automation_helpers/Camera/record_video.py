import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
import os

# Redirecting logs
log = logging.getLogger('debug_log')
log2 = logging.getLogger('info_log')


class perf_cam_cap:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_capture_pic(self):
        log2.info("==Entering into rear camera block==")
        (output, error, status) = cf.execute_commands("adb -s {0} logcat -c".format(self.Data["deviceId"][0]))
        if not status:
            return False, "Not executed"
            # Press HomeScreen
        home_cmd = f"adb -s {self.Data['serialId']} shell am start -W -c android.intent.category.HOME -a android.intent.action.MAIN"
        (output, error, status) = cf.execute_commands(home_cmd)

        time.sleep(2)
        # Opening Camera..
        log2.info("Opening camera..")
        cam_cmd = f"adb -s {self.Data['serialId']} shell am start -a android.media.action.VIDEO_CAPTUR"
        (output, error, status) = cf.execute_commands(cam_cmd)
        log.debug("Opening camera.. {0}".format(cam_cmd))

        time.sleep(5)
        # Capturing video
        log2.info("Video start to recording..")
        vid_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 25"
        (output, error, status) = cf.execute_commands(vid_cmd)
        log.debug("Video start to recording.. {0}".format(vid_cmd))

        time.sleep(5)
        vid_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 25"
        (output, error, status) = cf.execute_commands(vid_cmd)

        time.sleep(0)
        log2.info("Video recorded successfilly")
        vid_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 25"
        video = datetime.now().strftime("VID_%Y%m%d_%H%M%S")
        (output, error, status) = cf.execute_commands(vid_cmd)
        log.debug("Recorded video successfully {0}".format(vid_cmd))
        log2.info("File name stored as {0}.mp4".format(video))

        (output, error, status) = cf.execute_commands(home_cmd)
        time.sleep(5)
        log.debug("Browse the file {0}".format(video))
        os.system(f"adb -s {self.Data['serialId']} shell ls /storage/emulated/0/DCIM/Camera/{video}.mp4 > /dev/null 2>&1 && echo \"File is exists\" || echo \"File isn't exists\" ")
        # Browse and display the video
        log2.info("Opening the latest video {0}.mp4".format(video))
        view_cmd = f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.VIEW -d file:///storage/emulated/0/DCIM/Camera/{video}.mp4 -t video/*"
        (output, error, status) = cf.execute_commands(view_cmd)
        log.debug("Playing the latest video {0}".format(view_cmd))
        time.sleep(10)
        (output, error, status) = cf.execute_commands(home_cmd)
        time.sleep(2)
        #Delete the video
        log2.info("Deleted the latest video {0}.mp4".format(video))
        del_cmd = f"adb -s {self.Data['serialId']} shell rm /storage/emulated/0/DCIM/Camera/{video}.mp4 "
        (output, error, status) = cf.execute_commands(del_cmd)

        time.sleep(3)
        # Valudation of deleted picture
        log2.info("Valudation of deleted video {0}.mp4".format(video))
        time.sleep(2)
        os.system(f"adb -s {self.Data['serialId']} shell ls /storage/emulated/0/DCIM/Camera/{video} > /dev/null 2>&1 && echo \"File is exists\" || echo \"File isn't exists\" ")

        return True, "Rear Camera executed"

def record_video(tst, yamlData):
    call_obj = perf_cam_cap(tst, yamlData)
    status, msg = call_obj.execute_capture_pic()
    return status, msg
