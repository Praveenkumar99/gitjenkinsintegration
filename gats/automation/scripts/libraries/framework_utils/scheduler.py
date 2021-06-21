import json
import subprocess
import ast
import os
import sys
import time
import logging
import ruamel.yaml
import yaml
import signal
from database_query import Database
import log_utils
import platform
from device_info import execute_adb_cmd, locate_config, DeviceNotConnected, \
    UnknownDeviceConfig

import automation_helpers.globalconstants as gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = logging.getLogger(__name__)


class Scheduler:
    """
    class name     : Scheduler
    Description     : this class features the function API for scheduling
    the test run by receiving the test data from the json data
    :author: v.halli@globaledgesoft.com
    """
    device_id = None
    rum_yaml = ruamel.yaml.YAML()
    rum_yaml.indent(mapping=2, sequence=2)

    @staticmethod
    def get_device_data(data, key_, device):
        """
        :function name      : get_device_data
        :description        : gets the device information like macid, ip
                              name, testRunId, testRunName
        :param data:
        :param key_:
        :param device:
        :return:
        :author: v.halli@globaledgesoft.com
        """
        dict_value = None
        try:
            items = data["devices"][device]
            if str(items[key_]).strip() != "" and str(items[key_]) != 'None':
                dict_value = str(items[key_])
            return dict_value
        except TypeError:
            LOG.error("parameter data type should be dict got %s instead",
                      type(data))
            return dict_value
        except KeyError:
            LOG.error("No such %s key type", key_)
            return dict_value
        except ValueError:
            LOG.error("Passing None type value to key %s", key_)
            return dict_value
        except AttributeError as _ex_:
            LOG.error(_ex_)
            return dict_value

    @staticmethod
    def get_test_data(data, _key):
        """
        :function name      : get_test_data
        :description        : gets the specific data from the python
        dictionary object. The specific data such as sessionName, projectName
        milestone and device name which is necessary for script logging is
        extracted from the Dictionary object
        :param data         :Python dictionary object which acontains the key
        value pairs of test data
        :param _key         :field name whose value needs to be fetched
        :return dict_value  : return the dictionary value for the key
        :author: v.halli@globaledgesoft.com
        """
        dict_value = None
        try:
            if _key in "automation_id" or _key in "projectName" or \
                    _key in "milestone" or _key in "test_bed_name" or \
                    _key in "test_case_name" or _key in "TCP_UDP" or \
                    _key in "Bandwidth" or _key in "UL_DL" or _key in "HTTPS_LINK":
                if str(data[_key]).strip() != '' \
                        and str(data[_key]) != 'None':
                    dict_value = str(data[_key])
                else:
                    raise ValueError
            else:
                raise KeyError
            return dict_value
        except TypeError:
            LOG.error("parameter data type should be dict got %s instead",
                      type(data))
            return dict_value
        except KeyError:
            LOG.error("No such %s key type", _key)
            return dict_value
        except ValueError:
            LOG.error("Passing None type value to key %s", _key)
            return dict_value
        except AttributeError as _ex_:
            LOG.error(_ex_)
            return dict_value

    @staticmethod
    def copy_data(dest_folder, source_folder, file_folder):
        """
        :function name      : copy_data
        :description        : Copies the file/Folder from the source_folder path
                              to the dest_folder path
        :param dest_folder: string
        :param source_folder: string
        :param file_folder: string
        :return: NA
        :author: v.halli@globaledgesoft.com
        """
        try:
            file_name = os.path.join(source_folder, file_folder)
            operating_sys = platform.platform()
            os_type = operating_sys.split("-")[0]
            if os_type == "Linux":
                cmd = "cp -R %s %s" % (file_name, dest_folder)
            else:
                dest_folder = os.path.join(dest_folder, file_folder)
                cmd = "xcopy /isvy %s %s" % (file_name, dest_folder)
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (result, error) = p.communicate()
            if p.returncode == 0:
                LOG.info("Successfully copied")
                return
            else:
                LOG.info("Not copied")
        except Exception as e:
            LOG.info("Got error : %s " % str(e))

    @staticmethod
    def update_yml_using_key(file_name, section, key, value):
        """

        :param file_name: YAML config file path
        :param section: Name of the section to reffer
        :param key: Key name
        :param value: Value of the key
        :return: Boolean, debug level, message
        :author: v.halli@globaledgesoft.com
        """
        try:
            with open(file_name) as fp:
                common_yml = Scheduler.rum_yaml.load(fp)

            if common_yml.get(section):
                if common_yml[section].get(key):
                    common_yml[section][key] = value
                    with open(file_name, "w") as fp:
                        Scheduler.rum_yaml.dump(common_yml, fp)
                        return (True, "info",
                                "Provided key {0} of section {1} in yaml is"
                                " updated successfully {2}".format(key, section,
                                                                   value))
                return (True, "info",
                        "Provided key {0} not found in section {1} in yaml file"
                        .format(key, section))
            return (True, "info",
                    "Provided section {0} not found in yaml file "
                    .format(section))
        except KeyError as key_err:
            raise KeyError("Please provide proper key value. keyerror:{0}"
                           .format(key_err))

    @staticmethod
    def update_yaml(file_name, data):
        """
        Dumps the data as section into the yaml file
        :param file_name: YAML config file path
        :param data: Data to be dumped
        :return: Boolean, debug level, message
        :author: Sayyuf Shaik
        """
        try:
            with open(file_name, 'a+') as yaml_file:
                data_dict = {"yamlData": data}
                yaml.dump(data_dict, yaml_file)
                #print('Updating yaml file: {0} with data: {1}'.format(
                #    file_name, data))
        except KeyError as key_err:
            raise KeyError("Please provide proper key value. keyerror:{0}"
                           .format(key_err))

    @staticmethod
    def run(data):
        """
        :function name : run
        :description :The dictionary representation of test data will be
        received the tags will be extracted from this data. These tags will
        be send at a time to the run Module and the test will be executed.
        :author     :Vinay Halli
        :param data :Python data object- Dictionary data which is taken after
        parsing the JSON data from the cloud app
        :return robo_run:Return the sun status of the robot execution. This
        return value can further  be used as check for successful test suite run
        :author: v.halli@globaledgesoft.com
        """
        try:
            database_obj = Database()
            device_dict = data
            if type(data) == str:
                device_dict = ast.literal_eval(data)
            total_device = len(device_dict['devices'])
            print("total_device{}".format(total_device))
            task_list = []
            create_table = "CREATE TABLE IF NOT EXISTS Parallel_Proc_Info" \
                           "(DEVICE_ID" \
                           ", TESTEXEC_ID, FILE_PATH, PROCESS_ID)"

            database_obj.execute_query(create_table)
            # Function For Each Device
            for device in range(0, total_device):
                tags = device_dict["devices"][device]["testCase"]
                # Getting the devices dictionary
                device_data = device_dict["devices"][device]
                # Logic for multiple iterations
                multi_tags = []
                for tc, tc_count in tags[0].items():
                    for _ in range(tc_count):
                        multi_tags.append(tc)
                # print("Multi tags: {}".format(multi_tags))
                tags_to_include = multi_tags[0]
                for k in multi_tags[1:]:
                    tags_to_include = tags_to_include + "AND" + k
                print(f'Test cases to be Executed: {tags_to_include}')
                milestone = Scheduler.get_device_data(device_dict,
                                                      "mileStoneName", device)
                print("milestone:{}".format(milestone))
                if milestone is None:
                    milestone = "null"
                session_id = Scheduler.get_test_data(
                    device_dict, "automation_id")
                project_name = Scheduler.get_test_data(device_dict,
                                                       "projectName")
                device_name = Scheduler.get_device_data(device_dict, "deviceName",
                                                        device).replace(" ",   "_")
                test_run_id = Scheduler.get_device_data(device_dict,
                                                        "testRunId", device)
                mac_id = Scheduler.get_device_data(
                    device_dict, "macId", device)
                device_id = Scheduler.get_device_data(device_dict, "serialId",
                                                      device)
                print("device_id:{}".format(device_id))
                print("session_id:{}".format(session_id))
                print("project_name:{}".format(project_name))
                print("device_name:{}".format(device_name))

                # fetch device info like android version, manfacturer, model,
                # product.
                device_info = execute_adb_cmd(device_id)
                print("device_info:{}".format(device_info))
                # Fetching root folder path
                main_dir = os.path.abspath(
                    os.path.join(os.path.dirname(__file__),
                                 '..', '..', '..'))
                # folder structure path to be appended to root directory for
                # storing the logs and and reports based on device connected
                config_path = locate_config(device_info, main_dir)
                config_device_name = device_name + "_" +\
                    config_path.split("/")[2] + "_" +\
                    config_path.split("/")[3]

                # path of the folder to copy config and other related files
                input_image_path = log_utils.image_and_yaml_copy_dir(
                    project_name, session_id, config_device_name)
                yaml_path = os.path.join(input_image_path)
                print(f'yaml path:{yaml_path}')

                test_config_dir = os.path.abspath(os.path.join(main_dir, "results", project_name,
                                            "test_configuration", session_id, device_name ))
                # Add yaml path to globalconstants
                Scheduler.copy_data(input_image_path, main_dir, "inputs")
                Scheduler.copy_data(input_image_path, main_dir, config_path)
                Scheduler.copy_data(input_image_path, main_dir,
                                    "variables/variables_common.yaml")
                # file_to_read = os.path.join(input_image_path,
                #                             "variables_common.yaml")
                read_yaml = os.path.join(input_image_path,
                                         "uiconfig.yaml")
                print(f'input_image_path:{input_image_path}')
                # TODO : yaml_path and input_image_path are both same(If not need we can remove one)
                gc.INPUT_IMAGE_PATH = input_image_path
                Scheduler.update_yaml(read_yaml, device_data)
                print(f'After Updating uiconfig file: {read_yaml}')
                exec_status_path = Scheduler.start_execution(input_image_path,
                                                             device_name)
                # update_stopexec_file_path = \
                #     Scheduler.update_yml_using_key(file_to_read,
                #                                    "STOP_EXECUTION_FILE",
                #                                    "FILE_NAME",
                #                                    exec_status_path)
                # print(f'{update_stopexec_file_path}')

                cmd = r'python3.6 runner.py ' + \
                      os.path.join("..", "..", "robot_scripts") + ' -i '\
                      + tags_to_include + ' -v1 ' + str(project_name) + ' -v2 '\
                      + str(milestone) + ' -v3 ' + str(session_id) + ' -v4 ' +\
                      str(config_device_name) + ' -v5 ' + str(device_id) + \
                      ' -v6 ' + str(test_run_id) + ' -v7 ' + \
                      str(input_image_path) + ' -v8 ' + str(yaml_path) + \
                    ' -v9 ' + str(mac_id)

                with open(device_name+session_id+test_run_id+"_err.txt", "w")\
                        as stderr:
                    with open(device_name+session_id+test_run_id+"_out.txt",
                              "w") as stdout:
                        p = subprocess.Popen(cmd, stdout=stdout, shell=True,
                                             stderr=stderr)

                insert_query = "INSERT INTO Parallel_Proc_Info VALUES" \
                               " ('%s','%s','%s','%s')" % (str(device_id),
                                                           str(session_id),
                                                           str(exec_status_path),
                                                           str(p.pid))
                database_obj.execute_query(insert_query)
                task_list.append(p)

            while task_list:
                for process_id in task_list:
                    return_code = process_id.poll()
                    if return_code is not None:  # Process finished.
                        task_list.remove(process_id)
                        break
                    else:  # No process is done, wait a bit and check again.
                        time.sleep(.1)
                        continue
        except UnknownDeviceConfig:
            LOG.error("Detected unknown device. Please create respective device"
                      " variable directory and save the config file....!")
        except DeviceNotConnected:
            LOG.error("Please check the device connection and try again....!")
        except TypeError as _ex_:
            print("Error: ", _ex_)
            LOG.error("parameter data type should be dict got %s instead",
                      type(data))
        except(ValueError, NameError, KeyError, AttributeError) as _ex_:
            LOG.exception(_ex_)
        except RuntimeError as run_err:
            LOG.exception("RuntimeError:{0}".format(run_err))

    @staticmethod
    def start_execution(exec_dir, file_name):
        """
        :function name : start_execution
        :param exec_dir : json string
        :param file_name: file where the running status of a test execution is
                          saved
        :return: Python data object
        :author: Subhodeep
        """
        try:
            start_exec_path = (os.path.join(exec_dir, file_name)
                               + '_startexec.txt')
            with open(start_exec_path, 'w') as f:
                f.write('False')
            return start_exec_path
        except Exception as generic_except:
            LOG.exception(generic_except)

    @staticmethod
    def stop_execution(data):
        """
        :function name : stop_execution
        :param data : json string
        :return: Python data object
        :author: v.halli@globaledgesoft.com
        """
        database_obj = Database()
        try:
            for devices in data["deviceId"]:
                test_execid = str(data["testExecutionId"])
                device_id = str(devices)
                stop_exec_file = \
                    database_obj.fetch_stop_file_path(test_execid, device_id)
                with open(stop_exec_file, 'w') as f:
                    f.write('True')
        except Exception as generic_except:
            LOG.exception(generic_except)

    @staticmethod
    def kill_page(pid_id):
        """
        :param pid_id: Process Id to receive a kill signal
        :return: None
        :author: Subhodeep
        """
        pid = pid_id
        os.killpg(os.getpgid(pid), signal.SIGTERM)


if __name__ == '__main__':
    try:
        with open('read.json', 'r') as data_file:
            TEST_DATA = json.loads(data_file.read())
            print('**********************************************************')
            print("JSON Data: {}".format(TEST_DATA))
            print('**********************************************************')
            Scheduler.run(TEST_DATA)
    except (IOError, FileNotFoundError, FileExistsError)as _e_:
        LOG.exception("Failed to open %s file got %s error", 'read.json', _e_)
