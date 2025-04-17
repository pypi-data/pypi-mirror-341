import sys
import os

import json
import yaml


class RCSConfig:
    def __init__(self, argv):
        # 查找命令行参数指定配置文件
        cfg_file_path = None
        for i in range(len(argv)):
            if argv[i].endswith(".json"):
                print("config file is: ", argv[i])
                cfg_file_path = argv[i]
                break
            elif argv[i].endswith(".yaml"):
                print("config file is: ", argv[i])
                cfg_file_path = argv[i]
                break
        if cfg_file_path is not None:
            if cfg_file_path.endswith(".json"):
                self.parameters = self.read_from_json(cfg_file_path)
            elif cfg_file_path.endswith(".yaml"):
                self.parameters = self.read_from_yaml(cfg_file_path)
        else:
            # 没有查找到配置文件，则使用默认的配置文件
            self.parameters = self.read_from_yaml()

    def read_from_json(self, path="config.json"):

        # get current file path
        current_workspace_path = os.getcwd()
        print("current_workspace_path = \n", current_workspace_path)

        # 读取根目录的配置文件
        config_json_path = current_workspace_path + "/" + path
        print("config_json_path = \n", config_json_path)

        with open(config_json_path, "r", encoding="utf-8") as json_file:
            parameters = json.load(fp=json_file)

        # print json in beautiful format
        print("#################################")
        print("config.json is: ")
        print(json.dumps(parameters, indent=4, sort_keys=False))
        print("#################################")

        return parameters

    def read_from_yaml(self, path="config.yaml"):
        # get current file path
        current_workspace_path = os.getcwd()
        print("current_workspace_path = \n", current_workspace_path)

        # 读取根目录的配置文件
        config_yaml_path = current_workspace_path + "/" + path
        print("config_yaml_path = \n", config_yaml_path)

        with open(config_yaml_path, "r") as yaml_file:
            parameters = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # print yaml in beautiful format
        print("#################################")
        print("config.yaml is: ")
        print(yaml.dump(parameters, indent=4, sort_keys=False))
        print("#################################")

        return parameters


# Singleton Object
gl_rcs_config = RCSConfig(sys.argv)
