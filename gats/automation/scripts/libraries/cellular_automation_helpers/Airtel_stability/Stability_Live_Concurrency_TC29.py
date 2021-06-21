import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

#Redirecting logs
log = logging.getLogger(__name__)

class play_youtube_video:
    
    def __init__(self,tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def youtube_video_continue(self):

        log.info("starting to play youtube video...")
        status, msg = adb.stream_video(self.Data['serialId'], "START",
            self.Data['testcase_config'][self.tst]['HTTPS_LINK'])

        if not status:
            return False, msg

        #Waiting for youtube video to complete
        time.sleep(14400)
        #time.sleep(43000)


        status, msg = adb.stream_video(
            self.Data['serialId'], "STOP", None) 

        if not status:
            return False, msg

        log.info("Test Case executed")
        return True, 'Test Case executed'


def youtube_video_streaming(tst, yamlData):
    youtube_obj = play_youtube_video(tst, yamlData)
    status, msg = youtube_obj.youtube_video_continue()
    return status, msg 
