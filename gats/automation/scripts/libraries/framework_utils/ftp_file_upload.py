import os
import sys
import ftputil.session
from database_query import Database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from automation_helpers.common_utils import Utilities

class Uploadftp:
    """
    class name  : Uploadftp
    Description : This class features the function API for pushing log files
    to ftp server
    """
    DB = Database()

    def __init__(self):
        self.utils_obj = Utilities()

    def upload_dir(self, ftp_path_logs=None, choice=None):
        """
        Uploads the files in specified path to ftp server
        :param ftp_path_logs: path of the logs
        :param choice: test case logs/ robot logs
        :return: True/False
        """
        try:
            # logic to send testcase logs to ftp server
            if choice == "logs":
                sf = ftputil.session.session_factory(use_passive_mode=True)
                # session_factory (sf) used to generate FTP connections with
                # other factories than the default ftplib.FTP
                ip_addr = self.utils_obj.read_yml("IP", "FTP_IP")
                uname = self.utils_obj.read_yml("IP", "FTP_UNAME")
                pswrd = self.utils_obj.read_yml("IP", "FTP_PASSWD")
                path_dir = self.utils_obj.read_yml("IP", "FTP_LOG_DIR")
                with ftputil.FTPHost(ip_addr, uname, pswrd,
                                     session_factory=sf) as ftp_host:
                    for dir_name, _, dir_files in os.walk(ftp_path_logs):
                        local = os.path.join(os.curdir, dir_name)
                        remote = ftp_host.path.join(ftp_host.curdir,
                                                    dir_name).split('/results',
                                                                    1)[-1]
                        # getting the remote path
                        remote = path_dir + remote
                        if not ftp_host.path.exists(remote):
                            # making the directories that are in local path
                            ftp_host.makedirs(remote)
                        for files in dir_files:
                            local_files = os.path.join(local, files)
                            remote_files = ftp_host.path.join(remote, files)
                            if not ftp_host.path.exists(remote_files):
                                # uploading the files from local to ftp server
                                ftp_host.upload(local_files, remote_files)

            elif choice == "robot-logs":
                # logic to send robot logs to ftp server
                sf = ftputil.session.session_factory(use_passive_mode=True)
                # session_factory (sf) used to generate FTP connections with
                # other factories than the default ftplib.FTP
                ip_addr = self.utils_obj.read_yml("IP", "FTP_IP")
                uname = self.utils_obj.read_yml("IP", "FTP_UNAME")
                pswrd = self.utils_obj.read_yml("IP", "FTP_PASSWD")
                path_dir = self.utils_obj.read_yml("IP", "FTP_LOG_DIR")
                with ftputil.FTPHost(ip_addr, uname, pswrd,
                                     session_factory=sf) as ftp_host:
                    for dir_name, _, dir_files in os.walk(ftp_path_logs):
                        local = os.path.join(os.curdir, dir_name)
                        remote = ftp_host.path.join(ftp_host.curdir,
                                                    dir_name).split('/results',
                                                                    1)[-1]
                        # getting the remote path
                        remote = path_dir + remote
                        if not ftp_host.path.exists(remote):
                            # making the directories that are in local path
                            ftp_host.makedirs(remote)
                        for files in dir_files:
                            local_files = os.path.join(local, files)
                            remote_files = ftp_host.path.join(remote, files)
                            if not ftp_host.path.exists(remote_files):
                                # uploading the files from local to ftp server
                                ftp_host.upload(local_files, remote_files)
            else:
                print("Please enter a valid option. logs or robot-results")
        except Exception as generic_except:
            return "Failed to upload the files to ftp server {}"\
                .format(generic_except)
