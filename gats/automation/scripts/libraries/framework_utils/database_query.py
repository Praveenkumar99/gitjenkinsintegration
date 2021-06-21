import sqlite3
from sqlite3 import Error
import os
import json
import logging
import yaml
import csv
import re

LOG = logging.getLogger(__name__)


class Database(object):
    """
       class name     : Database
       Description     : this class features the function API for database
       query
    """
    mac_id = ""
    error = ""

    def __init__(self):
        try:
            db_name = Database.read_database_yml("DATABASE", "DATABASE_NAME")
            self.conn = sqlite3.connect(db_name, check_same_thread=False)
            self.curr = self.conn.cursor()
            self.create_user_table()
        except Error as _e:
            LOG.debug("Unable to establish Data base connection", _e)

    def go_to_database(self, get_test_result):
        """
        :function name : go_to_database
        :description : create a table if it does not exist
                       and push the data into the table
        :param get_test_result: json data containing device availability
                                status
        :return: None
        :author: s.subhodeep@globaledgesoft.com
        """
        try:
            LOG.debug("Inside method go_to_database")
            create_table = self.read_database_yml("QUERY".strip(),
                                                  "CREATE_TABLE".strip())
            table_name = self.read_database_yml("DATABASE", "TABLE_NAME")
            col1 = self.read_database_yml("DEVICE_STAT_COL", "COL1")
            col2 = self.read_database_yml("DEVICE_STAT_COL", "COL2")
            col3 = self.read_database_yml("DEVICE_STAT_COL", "COL3")
            col4 = self.read_database_yml("DEVICE_STAT_COL", "COL4")
            self.curr.execute(create_table.format(table_name, col1, col2, col3,
                                                  col4))

            self.curr.execute("INSERT INTO jason_dev_data (ip, macId, active,"
                              " message) "
                              "VALUES (" +
                              "%r" % str(get_test_result['ip']) + "," +
                              "%r" % get_test_result['macId'] + "," +
                              "%r" % str(get_test_result['active']) + "," +
                              "%r" % str(get_test_result['message']) + ")")
            self.conn.commit()
            self.curr.execute("SELECT * FROM jason_dev_data")
        except Exception as generic_except:
            LOG.debug("Got exception due to: {0}".format(generic_except))

    def get_table_data(self):
        """
        :function name : get_table_data
        :description : fetches the data from the database table
        :return: output i.e list of tuples
                 where each tuple contains each device
                 status information such as macId, IP
                 and activation status
        :author: s.subhodeep@globaledgesoft.com
        """
        table_name = self.read_database_yml("DATABASE", "TABLE_NAME")
        fetch_all = self.read_database_yml("QUERY", "FETCH_ALL")
        self.curr.execute(fetch_all.format(table_name))
        output = self.curr.fetchall()
        return output

    def get_data_count(self):
        """
        :function name : get_data_count
        :description : returns the number of rows present in the database table
        :return: count i.e the total number of rows present
                 in database table
        :author: s.subhodeep@globaledgesoft.com
        """
        table_name = self.read_database_yml("DATABASE", "TABLE_NAME")
        fetch_all = self.read_database_yml("QUERY", "FETCH_ALL")
        self.curr.execute(fetch_all.format(table_name))
        output = self.curr.fetchall()
        count = len(output)
        return count

    def delete_table(self):
        """
        :function name : delete_table
        :description : drops the database table for device status
        :return: None
        :author: Subhodeep
        """
        self.curr.execute("DROP TABLE jason_dev_data")
        LOG.info("Table Deleted successfully")

    def delete_test_table(self):
        """
        :function name : delete_test_table
        :description : drops the database table for test results
        :return: None
        :author: s.subhodeep@globaledgesoft.com
        """
        self.curr.execute("DROP TABLE test_res_table")
        LOG.info("Table Deleted successfully")

    @staticmethod
    def tuple_to_json(list_of_tup):
        """
        :function name : tuple_to_json
        :description : used to change the list of
                      tuples, which is fetched from database,
                      into list of dictionaries

        :param list_of_tup: list of tuples containing device
                              status data fetched from database
        :return: buffer i.e list of dictionaries
                 containing device availability status
        :author: Rajagonda
        """
        buffer = []
        for tups in list_of_tup:
            if tups[2] == 'True':
                dict_output = {"macId": tups[1], "ip": tups[0], "active": True,
                               "message": tups[3]}
            else:
                dict_output = {"macId": tups[1], "ip": None, "active": False,
                               "message": tups[3]}
            buffer.insert(list_of_tup.index(tups), dict_output)
        return buffer

    @staticmethod
    def set_mac(items):
        """
            :function name: set_mac
            :param items: receiving the mac id from the MQTT subscriber
                          and setting the same for the class variable mac_id
            :return: Returning back, if the mac id is set. Else returning false
            :author: Rajagonda

        """
        flag = False
        if items["macId"] is not None:
            Database.mac_id = items["macId"]
        if Database.mac_id != "":
            flag = True
        return flag

    @staticmethod
    def get_status(items):
        """
        get_status uses arp-scan tool to get the ip address for respective mac
        address
        :return: dictionary{mac:"xyz",ip:"xyz",active:True/False}
        :author: v.halli@globaledgesoft.com
        """
        try:
            ret_val = False
            ip_address = items["ip"]
            mac_id = Database.mac_id.lower()

            dev_stat = Database.verify(ip_address, mac_id)
            if dev_stat[0]:
                ret_val = {"macId": Database.mac_id, "ip": ip_address,
                           "active": True, "message": dev_stat[1]}
            else:
                if "Unable to perform SSH" in dev_stat[1]:
                    ret_val = {"macId": Database.mac_id, "ip": ip_address,
                               "active": False, "message": dev_stat[1]}
                elif dev_stat[1] == "Device configured incorrectly" or \
                        dev_stat[1] == "Device is unreachable":
                    ret_val = {"macId": Database.mac_id, "ip": ip_address,
                               "active": False, "message": dev_stat[1]}
            return ret_val
        except (TypeError, ValueError, OSError, IndexError) as _ex_:
            if isinstance(_ex_, IndexError):
                LOG.exception("Invalid Mac address")
                ip_address = None
                ret_val_error = {"macId": Database.mac_id, "ip": ip_address,
                                 "active": False,
                                 "message": "Exception was generated"}
                return ret_val_error
            else:
                LOG.exception(_ex_)
                ip_address = None
                ret_val_error = {"macId": Database.mac_id, "ip": ip_address,
                                 "active": False,
                                 "message": "Exception was generated"}
                return ret_val_error

    @staticmethod
    def verify(ip_address, mac_address=None):
        """
        :function name : verify
        :description : used to ping ip address and compare the macId id device
                        is reachable
        :param ip_address:
        :param mac_address:
        :return: (Bool, str)
        :author: s.subhodeep@globaledgesoft.com
        """
        from automation_helpers.common_utils import Utilities
        com_utils = Utilities()
        response = os.system("ping -c 1 {}".format(ip_address))
        if response == 0:
            ip_mac = com_utils.ssh_exe_cmd(
                "ifconfig | grep Ethernet | grep ^e | awk '{print $5}'",
                ip=ip_address)
            if ip_mac[0]:
                ip_mac[1] = ip_mac[1].strip('\n')
                if ip_mac[1] == mac_address:
                    return True, "Device is available"
                else:
                    return False, "Device configured incorrectly"
            else:
                return False, "Unable to perform SSH on the selected device"
        else:
            return False, "Device is unreachable"

    @staticmethod
    def json_parser(json_data):
        """
        :function name : json_parser
        :param json_data :
        :return: Python data object
        :author: Rajagonda
        """
        try:
            decoded_data = json.loads(json_data)
            return decoded_data
        except (ValueError, KeyError, TypeError):
            LOG.debug("JSON format error")

    @staticmethod
    def read_database_yml(section, option):
        """Used to read values from yaml files
        :param section: section name
        :param option: option name
        :return: string
        :author: Rajagonda, Vinay , Subhodeep
        """
        try:
            #print('section: {0} , option: {1}'.format(section, option))
            main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    "..", "..", ".."))
            path_var = os.path.join(main_dir, "variables/")
            common_yml = yaml.load(
                open(path_var + "variables_framework.yaml"), Loader=yaml.Loader)
            if section in common_yml.keys():
                if option in common_yml[section]:
                    return common_yml[section][option]
                return (False, "provided {0} option name "
                               "not found in given section "
                               "{1}".format(option, section))
            return (False, "provided section {0} not found "
                           "in yaml file ".format(section))
        except KeyError as key_err:
            raise KeyError("Please provide proper key value.keyerror:{0}".
                           format(key_err))

    def store_to_database(self, get_test_result):
        """
        :function name: store_to_database
        :param get_test_result: json object
        :return:
        :author: v.halli@globaledgesoft.com, s.subhodeep@globaledgesoft.com
        """
        try:
            print("Inside store_to_database")
            LOG.info("get_test_result:{}".format(get_test_result))
            create_table = self.read_database_yml("QUERY".strip(),
                                                  "CREATE_TEST_TABLE".strip())
            print("create_table:{}".format(create_table))
            print("After creating table")
            table_name = self.read_database_yml("DATABASE", "TEST_TABLE_NAME")
            LOG.info("table_name:{}".format(table_name))
            print("table_name:{}".format(table_name))
            col1 = self.read_database_yml("DEVICE_STAT_COL", "COL1")
            col2 = self.read_database_yml("DEVICE_STAT_COL", "COL20")
            col3 = self.read_database_yml("DEVICE_STAT_COL", "COL30")
            col4 = self.read_database_yml("DEVICE_STAT_COL", "COL40")
            col5 = self.read_database_yml("DEVICE_STAT_COL", "COL50")
            col6 = self.read_database_yml("DEVICE_STAT_COL", "COL60")
            col7 = self.read_database_yml("DEVICE_STAT_COL", "COL70")
            col8 = self.read_database_yml("DEVICE_STAT_COL", "COL80")
            col9 = self.read_database_yml("DEVICE_STAT_COL", "COL90")
            create_table_formated = create_table.format(table_name, col1, col2, col3,
                                col4, col5, col6,
                                col7, col8, col9)
            print('create table sql query: {}'.format(create_table_formated))
            self.curr.execute(create_table_formated)
            LOG.info(self.curr.execute("SELECT * FROM test_res_table"))
            print('TEST CREATE TABLE: {}'.format(self.curr.execute("SELECT * FROM test_res_table")))
            print("------------------------")
            LOG.info("*********************************")
            print('Get Test Result: {}'.format(get_test_result))
            LOG.info("get_test_result['macId'])", get_test_result['macId'])
            print("Before inserting in to test_res_table")
            self.curr.execute("INSERT INTO test_res_table "
                              "(macId, testRunId, result,"
                              "automationId,failureReason,startTime,"
                              "endTime,"
                              " testcaseCustomId, ftpLink) "
                              "VALUES (" +
                              "%r" % str(get_test_result['macId']) + "," +
                              "%r" % get_test_result['testRunId'] + "," +
                              "%r" % get_test_result['result'] + "," +
                              "%r" % get_test_result['automationId'] + "," +
                              "%r" % get_test_result['failureReason'] + "," +
                              "%r" % get_test_result['startTime'] + "," +
                              "%r" % get_test_result['endTime'] + "," +
                              "%r" % get_test_result['testcaseCustomId'] + "," +
                              "%r" % str(get_test_result['ftpLink']) + ")")
            LOG.info("Data Inserted successfully")
            print('After inserting into the database')
            self.conn.commit()
            self.curr.execute("SELECT * FROM test_res_table")
            LOG.info("In database::::: ", self.curr.fetchall())
            print('Done inserting into table.!!!!')
            return "Done"
        except sqlite3.Error as sql_err:
            logging.error("Data is not stored.Got error:{0}".format(sql_err))

    def fetch_from_dashboard(self, macid, test_case):
        """
        :function name: fetch_from_dashboard
        :param macid:
        :param test_case:
        :return:
        :author: s.subhodeep@globaledgesoft.com, v.halli@globaledgesoft.com
        """
        try:
            self.curr.execute("SELECT * FROM  test_res_table WHERE "
                              "(macId = %r AND testcaseCustomId = %r)"
                              % (macid, test_case))
            out = self.curr.fetchall()
            if not len(out) > 1:
                test_data = {"macId": out[0][1],
                             "testRunId": int(out[0][2]),
                             "result": out[0][3],
                             "automationId": int(out[0][4]),
                             "failureReason": out[0][5],
                             "startTime": out[0][6],
                             "endTime": out[0][7],
                             "testcaseCustomId": str(out[0][8]),
                             "ftplink": out[0][9]}
                return test_data, out[0][8], out[0][1]
            else:
                test_data = {"macId": out[1][1],
                             "testRunId": int(out[1][2]),
                             "result": out[1][3],
                             "automationId": int(out[1][4]),
                             "failureReason": out[1][5],
                             "startTime": out[1][6],
                             "endTime": out[1][7],
                             "testcaseCustomId": str(out[1][8]),
                             "ftplink": out[1][9]}
                return test_data, out[1][8], out[1][1]           
        except RuntimeError:
            raise RuntimeError("Error: Got Duplicate Entries")
        except sqlite3.Error as sql_err_:
            logging.error("Could not Fetch data.Got Error{0}".format(sql_err_))

    def del_query(self, test_case, macid):
        """
        :function name: del_query
        :param test_case:
        :param macid:
        :return:
        :author: s.subhodeep@globaledgesoft.com
        """
        LOG.info("Data of del query:: ", macid, test_case)
        self.curr.execute('''DELETE FROM  test_res_table
        WHERE ( macId = %r AND test_res_table = %r)''' % (macid, test_case))
        LOG.info("Deleted Successfully------------")
        self.curr.execute("SELECT * FROM test_res_table")
        LOG.info("In database after deleting::::: ", self.curr.fetchall())

    def execute_query(self, query):
        """
        :function name : execute_query
        :description : execute the database query
        :param query : contain a database query
        :return: None
        :author: k.krishna@globaledgesoft.com
        """
        try:
            self.curr.execute(query)
            self.conn.commit()
        except Exception as exp_err:
            LOG.error("Unable to execute query{0} got error {1}".
                      format(query, exp_err))

    def fetch_stop_file_path(self, test_execid, mac_id):
        """

        :param test_execid:
        :param mac_id:
        :return:
        """
        try:
            self.curr.execute("SELECT * FROM  Parallel_Proc_Info WHERE "
                              "(MAC_ID = %r AND TESTEXEC_ID = %r)"
                              % (mac_id, test_execid))
            out = self.curr.fetchall()
            return out[0][2]
        except RuntimeError:
            raise RuntimeError("Error: Got Duplicate Entries")
        except sqlite3.Error as sql_err_:
            logging.error("Could not Fetch data.Got Error{0}".format(sql_err_))

    def close_conn(self):
        """
        :function name: close_conn
        :return:
        """
        self.conn.close()
        LOG.info("Connection closed--------------")

    @staticmethod
    def writting_into_csv_file(data_list):
        """ writting_into_csv_file is used to write data to the csv file

        """
        csv_file = "data_to_csv_" + str(data_list[0][3]) + ".csv"
        if not os.path.exists(csv_file):
            file_obj = open(csv_file, "w")
            writer = csv.writer(file_obj)
            data_header = [["macId", "testRunId", "result", "testExecutionId",
                            "failureReason", "startTime", "endTime",
                            "testCaseId", "ftplink"]]
            writer.writerows(data_header)
            file_obj.close()
        with open(csv_file, "a") as writterFile:
            writer = csv.writer(writterFile)
            writer.writerows(data_list)
        writterFile.close()

    def create_user_table(self):
        """
        :function name : create_user_table
        :description : creates user table
        :return: None
        :author: s.subhodeep@globaledgesoft.com
        """
        self.curr.execute(
            "CREATE TABLE IF NOT EXISTS  USER_DATA(  DATA VARCHAR(200)"
            " PRIMARY KEY, STATUS VARCHAR(20) )")

    def insert_user(self, user_data, lock):
        """
        :function name : insert_user
        :description : inserts user data comming from dashboard
       :param user_data:
       :param lock: used for sync of processes accessing the database
       :return:
       :author: s.subhodeep@globaledgesoft.com
        """
        try:
            lock.acquire(blocking=False)
            var = "INSERT INTO USER_DATA(DATA, STATUS) VALUES(%r, 'NO')"\
                  % (user_data)
            self.curr.execute(var)
            self.conn.commit()
            lock.release()
        except Exception as _ex:
            print("Got Exception: {0}".format(_ex))
        

    def fetch_user_data(self):
        """
        :function name : fetch_user_data
        :description : fetch user data from USER_DATA table
       :return: user data in tuple format
       :author: s.subhodeep@globaledgesoft.com
        """
        q = "SELECT * FROM USER_DATA WHERE(STATUS = 'NO')"
        obj = self.curr.execute(q)
        x = obj.fetchall()
        return x

    def update_user_status(self, json_list):
        """
        :function name : update_user_status
        :description : updates the STATUS column in USER_DATA table
        :param json_list:
        :return:
        """
        try:
            quer = "UPDATE USER_DATA SET STATUS = 'YES' WHERE DATA IN " +\
                   str(json_list)
            self.curr.execute(quer)
            self.conn.commit()
            return True
        except Exception as _ex:
            return False, _ex
