"""
Browser
"""

import time
import logging
import automation_helpers.globalconstants as gc
import cellular_automation_helpers.common_helper_functions.common_functions as cf
import cellular_automation_helpers.common_helper_functions.adb_command_functions as adb
from datetime import datetime
import re

# Redirecting logs
log = logging.getLogger(__name__)



class browser:

    def __init__(self, tst, yamlData):
        self.tst = tst
        self.Data = yamlData

    def check_cache(self):
        log.info("Checking the cache..")
        (output, error, status) = cf.execute_commands(
            f"adb -s {self.Data['serialId']} shell su 0 ls -lh /data/data/com.android.chrome/cache/ > {gc.IMAGE_FOLDER}/browser.txt")
        time.sleep(5)
        cache_size = ''
        for line in open(f"{gc.IMAGE_FOLDER}/browser.txt", 'r+'):
            match = re.search('total (\d*\.?\d+)', line)
            if match:
                cache_size = match.group(1)
        if cache_size == '0':
            return 0
        return cache_size

    def browser_cache(self):
        (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} logcat -c")
        if not status:
            return False, "Not executed"
        log.info("Entering into Browser Cache Block")
        cache_size = self.check_cache()
        log.info("Size of the cache '{0} K'".format(cache_size))
        (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} shell su 0 rm -rf /data/data/com.android.chrome/cache/* > {gc.IMAGE_FOLDER}/browser.txt")
        log.info("Checking size of the cache '{0} K'".format(self.check_cache()))
        cache_size = self.check_cache()
        if cache_size == 0:
            log.info("Cache file is empty")
                
            # Launch Browser
            log.info("launching browser..")
            (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} shell am start -a android.intent.action.VIEW -d {self.Data['testcase_config'][self.tst]['HTTP_LINK']}")
            time.sleep(10)
            self.check_cache()
            if cache_size == '0':
                log.info("=======> Cache file not stored properly <=======")
            else:
                log.info("=======> Size of the cache '{0} K' <=======".format(self.check_cache()))

                log.info("Closing Browser")
                (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} shell am force-stop com.android.chrome")
        else:
            log.info("Clear the Cache file")
            (output, error, status) = cf.execute_commands(f"adb -s {self.Data['serialId']} shell su 0 rm -rf /data/data/com.android.chrome/cache/* > {gc.IMAGE_FOLDER}/browser.txt")
            log.info("Checking size of the cache '{0} K'".format(self.check_cache()))
            log.info("========> Clear the cache successfully <========")
            time.sleep(5)

        return True, "Browser clear cache executed successfully"

def browser_cache(tst, yamlData):
    call_obj = browser(tst, yamlData)
    status, msg = call_obj.browser_cache()
    return status, msg
