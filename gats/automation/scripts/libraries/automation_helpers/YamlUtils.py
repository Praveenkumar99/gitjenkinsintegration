# added to suppress the pylint error related to print in python 3
import os
import logging
import sys
import yaml
import yamlordereddictloader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import automation_helpers.globalconstants as gc
from automation_helpers.common_log import common_log


log = logging.getLogger(__name__)


class YamlUtils:

    @staticmethod
    def read_yml_using_section(section):
        """Used to read values from yaml files using only section name to fetch
        all the options with value pairs
        :param section: section name
        :return: string
        """
        try:
            main_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '..', '..', '..'))
            path_var = os.path.join(main_dir, "variables")
            # loads all the options and values of section in dictionary format
            common_yml = yaml.load(open(os.path.join(path_var,
                                                     "variables_common.yaml")),
                                   Loader=yamlordereddictloader.Loader)
            print(common_yml)
            if section in common_yml.keys():
                return common_yml[section]
            return common_log.return_values(True, "info",
                                            "Provided section {0} not found in yaml"
                                            " file ".format(section))
        except KeyError as key_err:
            raise KeyError("Please provide proper key value. keyerror:{0}".
                           format(key_err))

    @staticmethod
    def read_yml(section, option, path=None):
        """
        Used to read values from yaml files
        :param section: section name
        :param option: option name
        :return: string
        """
        try:
            log.debug("Inside read_yml method")
            if path is None:
                file_path = gc.YAML_PATH
            else:
                file_path = path
            if not gc.YAML_OBJ:
                with open(os.path.join(file_path, "uiconfig.yaml")) as ymlfile:
                    gc.YAML_OBJ = yaml.safe_load(ymlfile)
            if section in gc.YAML_OBJ.keys():
                if option in gc.YAML_OBJ[section]:
                    return gc.YAML_OBJ[section][option]
                log.error("provided {0} option name not found in given "
                          "section {1}".format(option, section))
                return False
            log.error("provided section {0} not found in yaml file"
                      .format(section))
            return False
        except KeyError as key_err:
            raise KeyError("Please provide proper key value.keyerror:{0}".
                           format(key_err))
        except Exception as generic_except:
            raise Exception("Exception occured due to :{}".
                            format(generic_except))

