# -*- coding: utf-8 -*-

"""
Function: 获取配置文件中的配置项
"""
import configparser
from os import path


def get_conf(config_file_name ,section, key):
    config_path = path.join(path.dirname(path.abspath(__file__)), config_file_name + '.ini')
    config = configparser.ConfigParser()
    config.read(config_path)
    result = config[section][key]
    return result
