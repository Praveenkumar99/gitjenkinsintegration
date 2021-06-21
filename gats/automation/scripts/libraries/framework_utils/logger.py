"""

"""

from datetime import datetime
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Logger:
    """
         :class name : Logger
             :description: Contains function api related to logging system log
                           files

    """

    def log_time_format(self, time_fmt):
        """
        :function name  : get_system_time
            :description    : this function is used get the system time
            :return         : string ....  #system time as 'HH:MM:SS'
            :author         : s.subhodeep@globaledgesoft.com

        """
        value1, value2 = time_fmt.split('PDT')
        datetime_object = datetime.strptime(value1.strip(), '%a %b %d %H:%M:%S')
        new_obj = datetime_object.strftime('%b %d')
        return new_obj

    def collect_log(self, start, stop, file_name):
        """
        :function name  :  collect_log
        :description    :  this function is used to collect logs from system
                            log file within the range of specific timestamps
                             and put it in a usermade *.log file
        :param          :   start and stop timestaps for logs to be
                            collected from system log file and the log file name
        :param file_name	:  complete path of the file
        :return		:  NA
        :author: s.subhodeep@globaledgesoft.com

        """
        output_filename = os.path.normpath("parsed_line.log")
        logger_file = os.path.join("/var/log", file_name)

        with open(output_filename, "w") as out_file:
            out_file.write("")

        with open(output_filename, "a") as out_file:
            with open(logger_file, "r") as in_file:
                use = False
                for line in in_file:
                    if datetime.now().strftime('%d') in line:
                        line_element = line.split()
                        if start <= line_element[2]:
                            use = True
                        if not stop > line_element[2]:
                            use = False
                        if use:
                            out_file.write(line)

    def clear_log_files(self, flag):
        """
        :function name  :  clear_log_files
        :description    :  Clear the syslog file present in /var/log
                           directory of ThinClient
        :param flag:    Boolean
        :return:
        :author: s.subhodeep@globaledgesoft.com
        """
        try:
            from automation_helpers.common_utils import Utilities
            com_utils = Utilities()
            if flag in ("True", "true"):
                output = com_utils.ssh_exe_cmd(
                    "echo admin| sudo --stdin truncate -s0 /var/log/syslog")
                if output[0]:
                    return True, "Log Files Successfully cleared"
                else:
                    return False, "Got Error:{0}".format(output[1])
        except Exception as gen_exc:
            return False, "Got Exception:{0}".format(gen_exc)

    def get_log_file(self, flag, dest_file):
        """
        :function name  :   get_log_file
        :description    :  fetches the syslog file present in /var/log
                           directory of ThinClient
        :param flag:       Boolean
        :param dest_file:  Destination folder for fetched syslog
        :return:
        :author: s.subhodeep@globaledgesoft.com
        """
        try:
            from automation_helpers.common_utils import Utilities
            com_utils = Utilities()
            if flag in ("True", "true"):
                output = com_utils.ssh_exe_cmd("cat /var/log/syslog")
                if output[0]:
                    sys_file = "ThinClient_syslog" + "_" \
                               + time.strftime('%Y%m%d-%H%M%S')
                    with open(os.path.join(dest_file, sys_file), "w")\
                            as dest_file:
                        dest_file.write(output[1])
                else:
                    return False, "Got Error:{0}".format(output[1])
        except Exception as gen_exc:
            return False, "Got Exception:{0}".format(gen_exc)

