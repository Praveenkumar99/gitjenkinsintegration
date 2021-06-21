import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)

class perform_switch_camera_video:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def execute_camera_video(self):
        log.debug("Entering into rear camera block")
        cmd = f"adb -s {self.Data['serialId']} logcat -c"
        (output, error, status) = cf.execute_commands(cmd)
        
        
        if not status:
            return False, "Not executed"
      
        log.info("Switching To Camera Mode")
        cmd = f"adb -s {self.Data['serialId']} shell am start android.media.action.IMAGE_CAPTURE"
        (output, error, status) = cf.execute_commands(cmd)
        if not status:
            return False, "camera is not opened"
        time.sleep(5)

        log.info("Switching To Video Mode")
        cmd = f"adb -s {self.Data['serialId']} shell am start -a android.media.action.VIDEO_CAPTURE"
        (output, error, status) = cf.execute_commands(cmd)
        time.sleep(4)

        if not status:
            return False, "Fail To Switch To Video Mode"

        log.info("Closing the application")
        cmd = f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.MAIN -c android.intent.category.HOME"
        (output, error, status) = cf.execute_commands(cmd)
        time.sleep(2)

        if not status:
            return False, " Test case not executed"

        return True, "Test case executed.."

def switch_camera_to_video(tst, yamlData):   
    camera_video_obj = perform_switch_camera_video(tst, yamlData)
    status, msg = camera_video_obj.execute_camera_video()    
    return status, msg
