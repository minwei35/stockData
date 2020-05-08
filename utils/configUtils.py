import configparser
import os

# os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 获取当前文件所在目录的绝对路径 注意：该路径不包含当前目录
parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 获取配置文件的的绝对路径
path = parentDirPath+'\\config\\config.ini'
cfg = configparser.ConfigParser()
cfg.read(path)


def get_config_value(section, key):
    return cfg.get(section, key)


def get_config_value_int(section, key):
    return cfg.getint(section, key)


def get_config_value_float(section, key):
    return cfg.getfloat(section, key)


def get_config_value_boolean(section, key):
    return cfg.getboolean(section, key)

