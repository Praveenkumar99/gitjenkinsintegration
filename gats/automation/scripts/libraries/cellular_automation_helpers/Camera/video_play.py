import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class play_video:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def preload_video(self):
        log.info("Preloading Video Files to Device")
        (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} push ../../../inputs/video/* /storage/emulated/0/Movies")
        if not status:
            return False, "Unable to preload video files"
        return True, "Preloaded Video Files"

    def execute_video_test(self):
        log.debug("Entering into Video block")
        cmd = f"adb -s {self.Data['serialId']} logcat -c"
        (output, error, status) = cf.execute_commands(cmd)
        if not status:
            return False, "Not executed"

        video_format = ["avi", "mp4", "mp4", "3gp"]
        for i in range(1, len(video_format)+1):
            status, msg = adb.play_video(deviceId=self.Data['serialId'],
                                         video_file_path=f"file:///storage/self/primary/Movies/test_{i}."+video_format[i-1],
                fileFormate="video/"+video_format[i-1])

            if not status:
                return False, msg

            status, msg = adb.stop_media(deviceId=self.Data['serialId'])

            if not status:
                return False, msg

        return True, "Test case executed"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])


def video_play(tst, yamlData):
    video_obj = play_video(tst, yamlData)
    status, msg = video_obj.preload_video()
    status, msg = video_obj.execute_video_test()
    if not status:
        video_obj.closeUp()
    return status, msg
