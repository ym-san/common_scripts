#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import re
import os
import json
import pandas as pd


def OpenJson(dir, filepath):
    dir_name = os.path.dirname(os.path.abspath(dir)) 
    path = os.path.join(dir_name, filepath)
    file = open(path, 'r')
    return json.load(file)

def OpenConfig():
    return OpenJson(__file__, 'config/config.json')

def CombPath(path,file):
    path_reg = (r'\/$')
    path = re.sub(path_reg, "", path)
    file_reg = (r'^\/')
    file = re.sub(file_reg, "", file)
    return path + '/' + file

def CheckDir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
        os.chmod(dir, 0o777)

def ChmodFile(file):
    os.chmod(file, 0o777)

def CheckFile(file):
    if  os.path.isfile(file):
        os.remove(file)

def CheckCombDir(path,dir):
    combdir = CombPath(path,dir)
    CheckDir(combdir)
    return combdir

def CheckCombFile(path,file):
    combfile = CombPath(path,file)
    CheckFile(combfile)
    return combfile

def SeparateFileName(filename):
    name_list = []
    name_list.append(filename.split("_")[0])
    name_list.append(filename.split("_")[1])
    name_list.append(filename.split("_")[2])
    name_list.append(filename.split("_")[3])
    name_list.append(filename.split("_")[4])
    name_list.append(filename.split("_")[5])
    return name_list

def CreateFileName(filename_list,filetype):
    filename = "_".join(filename_list) + filetype
    return filename

def ReadCsv(path, file):
    return pd.read_csv(CombPath(path, file), index_col=0)

def CreateCsvFromDf(df, path, file):
    df = df.sort_index()
    df.to_csv(CombPath(path, file))

def CreateCsvFromList(df_list, index_list, col_list, filename_list, path):
    df = pd.DataFrame(df_list)
    df.index = index_list
    df.columns = col_list
    outputfile = CreateFileName(filename_list,'.csv')
    CreateCsvFromDf(df, path, outputfile)
    return outputfile

def UpdateCsv(df, path, filename_list):
    outputfile = CreateFileName(filename_list, '.csv')
    CheckCombFile(path, outputfile)
    df = df.sort_index()
    df.to_csv(CombPath(path, outputfile))
    ChmodFile(CombPath(path, outputfile))
    return outputfile


config_data = OpenConfig()

LOG_FILE = config_data["log"]["path"]
LOG_LEVEL = config_data["log"]["level"]

class logger:
    def __init__(self, name=__name__):

        if LOG_LEVEL == "DEBUG": 
            level = logging.DEBUG
        elif LOG_LEVEL == "INFO": 
            level = logging.INFO
        else: 
            level = logging.ERROR

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s] %(message)s")

        handler = logging.handlers.RotatingFileHandler(filename = LOG_FILE)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    # def warn(self, msg):
    #     self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    # def critical(self, msg):
    #     self.logger.critical(msg)
