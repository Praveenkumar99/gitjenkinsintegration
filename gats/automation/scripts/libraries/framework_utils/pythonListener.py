"""

"""

import time
import sys
import os
from datetime import datetime
#from ftp_file_upload import Uploadftp
#from main_file_queue import MainQueue
from database_query import Database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import automation_helpers.globalconstants as globalconstants
from logger import Logger

class PythonListener(object):
    """
          class name      :   PythonListener
          Description     : this class features the function API for sending
                            robot-framework test results dynamically
    """
    ROBOT_LISTENER_API_VERSION = 3
    pass_counter = 0
    fail_counter = 0
    #QU = MainQueue()
    OBJ = Database()
    #FTP = Uploadftp()
    log_obj = Logger()

    def start_test(self, test, result):
        """
        :function name : start_test
        :description : This function interrupts the test-execution post running
                       to clear syslog files of Thinclient.
        :param test:
        :param result:
        :return:
        :author: s.subhodeep@globaledgesoft.com
        """
        flag = self.OBJ.read_database_yml("PASSWORD", "SYS_FLAG")
        PythonListener.log_obj.clear_log_files(flag)

    def end_test(self, data, result):
        """
        :function name : end_test
        :description : This function populates the result of the test execution
                       at the end of each test.
        :param data: contains the test information
        :param result: contains the execution result(PASS/FAIL)
        :return: None
        :author: Vinay, s.subhodeep@globaledgesoft.com
        """
        # from automation_helpers.common_utils import Utilities
        # utils_obj = Utilities()
        print("Time at the start of end_test method:{0}".format(datetime.now()))
        if result.passed:
            self.pass_counter = self.pass_counter + 1
            status = "PASSED"
            message = "PASSED"
        else:
            self.fail_counter = self.fail_counter + 1
            status = "FAILED"
            
            #status, msg = modem_logs.modem_logging(data, "STOP_START")
            message = result.message[:200] + (result.message[200:] and '..')

        start_time = PythonListener.epoch_time(result.starttime)
        end_time = PythonListener.epoch_time(result.endtime)
        try:
            user_log_path = globalconstants.LOG_FILE_PATH
            flag = self.OBJ.read_database_yml("PASSWORD", "SYS_FLAG")
            PythonListener.log_obj.get_log_file(flag, user_log_path)
            user_log_path2 = user_log_path.split("results")[1]
            # ftp_ip = utils_obj.read_yml("IP", "FTP_IP")
            # ftp_link = "ftp://"+ftp_ip+"/taf-results/result_logs" + \
            #            user_log_path2
            if "Execution was stopped from dashboard" in message:
                mac_id = globalconstants.MAC_ID
                test_execution_id = globalconstants.TEST_EXE_ID
                test_stop_json = {"testExecutionId": int(test_execution_id),
                                  "macId": str(mac_id)}
                #self.QU.publish_stop_execution(test_stop_json)
            if "Test execution stopped due to a fatal error" not in message:
                # self.FTP.upload_dir(globalconstants.IMAGE_FOLDER, "logs")
                pass
            # TODO uncomment below lines of code after FTP is setup
            '''csv_data_list = [[globalconstants.MAC_ID,
                              globalconstants.TEST_RUN_ID, status,
                              globalconstants.TEST_EXE_ID,
                              message, start_time, end_time,
                              result.tags[0], ftp_link]]'''
            csv_data_list = [[globalconstants.MAC_ID,
                              globalconstants.TEST_RUN_ID, status,
                              globalconstants.TEST_EXE_ID,
                              message, start_time, end_time,
                              result.tags[0]]]
            self.OBJ.writting_into_csv_file(csv_data_list)
            # TODO uncomment below lines of code after FTP is setup
            '''self.info_to_db(status, message, start_time, end_time,
                            result.tags[0], ftp_link)'''
            self.info_to_db(status, message, start_time, end_time,
                            result.tags[0])
            print("Time at the end of end test:{0}".format(datetime.now()))
        except Exception as ftp_err:
            print("Failed to upload files.Got Error:{0}".format(ftp_err))
            ftp_link = "Logs File Not Created. Check robot_results directory"
            csv_data_list = [[globalconstants.MAC_ID,
                              globalconstants.TEST_RUN_ID, status,
                              globalconstants.TEST_EXE_ID,
                              message, start_time, end_time,
                              result.tags[0], ftp_link]]
            self.OBJ.writting_into_csv_file(csv_data_list)

            self.info_to_db(status, message, start_time, end_time,
                            result.tags[0], ftp_link)

    def info_to_db(self, status, message, start_time, end_time,
                   test_case, ftp_link):
        """
        :function name : info_to_db
        :description : This function is used to store test case result into
                       database then publish the results to dashboard.
        :param status:
        :param message:
        :param start_time:
        :param end_time:
        :param test_case:
        :param ftp_link:
        :return:
        :author: s.subhodeep@globaledgesoft.com
        """
        mac_id = globalconstants.MAC_ID
        test_run_id = globalconstants.TEST_RUN_ID
        test_execution_id = globalconstants.TEST_EXE_ID
        '''test_data_json = {"macId": str(mac_id),
                          "testRunId": int(test_run_id),
                          "result": status,
                          "testExecutionId": int(test_execution_id),
                          "failureReason": message,
                          "startTime": start_time,
                          "endTime": end_time,
                          "testCaseId": str(test_case),
                          "ftplink": ftp_link}'''
        test_data_json = {"macId": str(mac_id),
"testRunId":int(test_run_id),
"result":status,
"automationId":int(test_execution_id),
"failureReason":message,
"startTime":str(start_time),
"endTime":str(end_time),
"testcaseCustomId": str(test_case),
"ftpLink":"None"}
        print("test_data_json:{}".format(test_data_json))
        stat = self.OBJ.store_to_database(test_data_json)
        print("stat:{}".format(stat))
        if stat == "Done":
            json_obj, ret_test_case, ret_mac, = self.OBJ.fetch_from_dashboard(
                mac_id, test_case)
            print("Before calling publish data")
            #self.QU.publish_data(json_obj)

    @staticmethod
    def epoch_time(time_val):
        """
        :function name : epoch_time
        :description : This function acts as an epoch time converter
        :param time_val: the start and ending time of test case
        :return: epoch_time
        :author: s.subhodeep@globaledgesoft.com
        """
        (_dt, _time) = time_val.split('.')
        date = datetime.strptime(_dt, '%Y%m%d %H:%M:%S')
        epoch_time = int(time.mktime(date.timetuple()) * 1000 + int(_time) * 10)
        print(str(epoch_time))
        # if you encounter a "year is out of range" error the timestamp
        # may be in milliseconds, try `ts /= 1000` in that case
        #print(datetime.utcfromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S'))
        return str(epoch_time)
