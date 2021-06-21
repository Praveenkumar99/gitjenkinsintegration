import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
import os

# Redirecting logs
log = logging.getLogger(__name__)



class perf_cam_cap:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_capture_pic(self):
        log.info("==Entering into rear camera block==")
        # Press HomeScreen
        home_cmd = f"adb -s {self.Data['serialId']} shell am start -W -c android.intent.category.HOME -a android.intent.action.MAIN"
        (output, error, status) = cf.execute_commands(home_cmd)

        time.sleep(2)
        # Opening Camera..
        log.info("Opening camera..")
        cam_cmd = f"adb -s {self.Data['serialId']} shell am start -a android.media.action.VIDEO_CAPTURE"
        (output, error, status) = cf.execute_commands(cam_cmd)
        log.debug("Opening camera.. {0}".format(cam_cmd))

        time.sleep(5)
        # Capturing video
        log.info("Video start to recording..")
        vid_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 25"
        (output, error, status) = cf.execute_commands(vid_cmd)
        log.debug("Video start to recording.. {0}".format(vid_cmd))

        time.sleep(5)
        vid_cmd = f"adb -s {self.Data['serialId']} shell input keyevent 25"
        (output, error, status) = cf.execute_commands(vid_cmd)

        time.sleep(5)
        log.info("Video recorded successfilly")
        browse = f"adb -s {self.Data['serialId']} shell ls -t /storage/emulated/0/DCIM/Camera | head -1 > {gc.IMAGE_FOLDER}/video_file.txt"
        (output, error, status) = cf.execute_commands(browse)
        camera = open('{0}/video_file.txt'.format(gc.IMAGE_FOLDER), 'r+')
        video = camera.readline()
        video = video[:-1]
        log.info("File name stored as {0}".format(video))

        (output, error, status) = cf.execute_commands(home_cmd)
        time.sleep(5)
        log.debug("Browse the file {0}".format(video))
        os.system(f"adb -s {self.Data['serialId']} shell ls /storage/emulated/0/DCIM/Camera/{video}> /dev/null 2>&1 && echo \"File is exists\" || echo \"File isn't exists\" ")
        # Browse and display the video
        log.info("Opening the latest video {0}.mp4".format(video))
        view_cmd = f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.VIEW -d file:///storage/emulated/0/DCIM/Camera/{video} -t video/*"
        (output, error, status) = cf.execute_commands(view_cmd)
        log.debug("Playing the latest video {0}".format(view_cmd))
        time.sleep(10)
        (output, error, status) = cf.execute_commands(home_cmd)
        time.sleep(2)
        #Delete the video
        log.info("Deleted the latest video {0}".format(video))
        del_cmd = f"adb -s {self.Data['serialId']} shell rm /storage/emulated/0/DCIM/Camera/{video} "
        (output, error, status) = cf.execute_commands(del_cmd)

        time.sleep(3)
        # Valudation of deleted picture
        log.info("Valudation of deleted video {0}".format(video))
        time.sleep(2)
        os.system(f"adb -s {self.Data['serialId']} shell ls /storage/emulated/0/DCIM/Camera/{video} > /dev/null 2>&1 && echo \"File is exists\" || echo \"File isn't exists\" ")

        return True, "Rear Camera executed"

def record_video(tst, yamlData):
    call_obj = perf_cam_cap(tst, yamlData)
    status, msg = call_obj.execute_capture_pic()
    return status, msg
