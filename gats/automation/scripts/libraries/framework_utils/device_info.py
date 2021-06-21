import subprocess
import os
import logging

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG = logging.getLogger(__name__)

class UnknownDeviceConfig(Exception):
    pass


class DeviceNotConnected(Exception):
    pass


def execute_adb_cmd(device_id):
    """
    This function is used to get device details using adb getprop
    :param device_id: Device id of android device to be tested
    :return: list:[android version, manufacturer, product model, product name]
    """
    try:
        l1 = []
        command = 'adb -s {0} shell getprop | grep "build.version.release\|' \
                  'product.manufacturer\|product.model\|product.name"'.\
            format(device_id)
        out = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        ).communicate()[0]
        adb_output = out.decode("utf-8").replace("\n", ",")
        if adb_output == "":
            raise DeviceNotConnected
        for r in (("[", "\'"), ("ro.", ""), (" ", ""), ("]", "\'")):
            adb_output = adb_output.replace(*r)
        adb_substring = (adb_output[:len(adb_output) - 1])
        # Splitting the string based on , we get key value pairs
        list1 = adb_substring.split(",")
        for i in list1:
            # Get Key Value pairs separately to store in dictionary
            key_value = i.split(":")
            res = key_value[1].strip('\'').split(".")[0]
            l1.append(res)
        return l1
    except IndexError as index_errror:
        LOG.exception("Exception due to :{}", format(index_errror))

def locate_config(device_info_list, variables_root_path):
    try:
        merged_info = "android_version_{0}/{1}/{2}/{3}".\
            format(device_info_list[0], device_info_list[1], device_info_list[2],
                   device_info_list[3])
        if os.path.exists(os.path.join(variables_root_path, "variables",
                                       merged_info)):
            #return os.path.join(variables_root_path, merged_info)
            return "variables/{0}/uiconfig.yaml".format(merged_info)

        print("To add config for this device, create following directory structure under variables directory")
        print(merged_info)
        raise UnknownDeviceConfig
    except IndexError as index_errror:
        LOG.exception("Exception due to :{}", format(index_errror))
