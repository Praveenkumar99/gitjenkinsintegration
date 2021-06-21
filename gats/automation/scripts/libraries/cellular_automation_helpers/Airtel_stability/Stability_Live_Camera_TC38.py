import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime

# Redirecting logs
log = logging.getLogger(__name__)


class play_audio:
    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def preload_audio(self):
        log.info("Preloading Audio Files to Device")
        (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} push ../../../inputs/audio/* /storage/emulated/0/Music")
        if not status:
            return False, "Unable to preload audio files"
        return True, "Preloaded Audio Files"

    def execute_audio_test(self):
        log.info("Entering into Video block")
        cmd = f"adb -s {self.Data['serialId']} logcat -c"
        (output, error, status) = cf.execute_commands(cmd)
        if not status:
            return False, "Not executed"

        audio_format = ["mp3", "mp3", "mp3", "mp3"]
        for i in range(1, len(audio_format)+1):
            status, msg = adb.play_audio(
                deviceId=self.Data['serialId'],
                audio_file_path=f"file:///storage/self/primary/Music/test_automation_{i}."+audio_format[i-1],
                fileFormate="audio/"+audio_format[i-1])

            if not status:
                return False, msg

            status, msg = adb.stop_media(deviceId=self.Data['serialId'])

            if not status:
                return False, msg

        return True, "Test case executed"

    def closeUp(self):
        # Graceful disconnection of call from Device A and B
        adb.graceful_disconnection(deviceId=self.Data['serialId'])


def audio_play(tst, yamlData):

    video_obj = play_audio(tst, yamlData)
    status, msg = video_obj.preload_audio()
    status, msg = video_obj.execute_audio_test()
    if not status:
        video_obj.closeUp()
    return status, msg
