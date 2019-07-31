#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import re
import os
import shutil
import json
import pandas as pd

# JSONを開く
def OpenJson(dir, filepath):
    dir_name = os.path.dirname(os.path.abspath(dir)) 
    path = os.path.join(dir_name, filepath)
    file = open(path, 'r')
    return json.load(file)

# Configを開く
def OpenConfig():
    return OpenJson(__file__, './config/config.json')

# LOG
config_data = OpenConfig()

LOG_FILE = config_data["path"]["log"]
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

# Pathの結合
def CombPath(path,file):
    path_reg = (r'\/$')
    path = re.sub(path_reg, "", path)
    file_reg = (r'^\/')
    file = re.sub(file_reg, "", file)
    return path + '/' + file

# ディレクトリが存在しなかったら作る
def CheckDir(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
        os.chmod(dir, 0o777)

#ファイルの権限を変更する
def ChmodFile(file):
    os.chmod(file, 0o777)

# ファイルが存在していたら消す
def CheckFile(file):
    if  os.path.isfile(file):
        os.remove(file)

# パス＋ディレクトリが存在しなかったら作る
def CheckCombDir(path,dir):
    combdir = CombPath(path,dir)
    CheckDir(combdir)
    return combdir

# パス＋ファイルが存在していたら消す
def CheckCombFile(path,file):
    combfile = CombPath(path,file)
    CheckFile(combfile)
    return combfile

# ファイル名を分解する
def SeparateFileName(filename):
    name_list = []
    name_list.append(filename.split("_")[0])
    name_list.append(filename.split("_")[1])
    name_list.append(filename.split("_")[2])
    name_list.append(filename.split("_")[3])
    name_list.append(filename.split("_")[4])
    name_list.append(filename.split("_")[5])
    return name_list

# ファイル名を作成する
def CreateFileName(filename_list,filetype):
    filename = "_".join(filename_list) + filetype
    return filename

# 正規表現で抽出
def SearchReg(line, reg):
    m = re.search(reg, line)
    return m.group(1)

# ファイルを読み取り専用で開いて全て抽出
def CreateFileAll(path, file, log):
    with open(CombPath(path, file),'r') as f:
        f_all = f.read()
    log.debug('READ ' + CombPath(path, file))
    return f_all

# ファイルを読み取り専用で開いてlinesを抽出
def CreateFileLines(path, file, log):
    with open(CombPath(path, file),'r') as f:
        lines = f.readlines()
    log.debug('READ ' + CombPath(path, file))
    return lines

# ファイルに追記する
def AddFileData(path, file, message):
    with open(CombPath(path, file), 'a') as f:
        f.write(message)

# CSVを読み込む
def ReadCsv(path, file, log):
    csv = pd.read_csv(CombPath(path, file), index_col=0)
    log.debug('READ ' + CombPath(path, file))
    return csv

# ファイルを移動する
def MoveFile(file, fromPath, toPath, log):
    CheckCombFile(toPath,file)
    shutil.move(CombPath(fromPath, file), toPath)
    log.debug('MOVE ' + CombPath(fromPath, file) + " " + toPath)

# ファイルを上書きコピーする
def Copy2File(file, fromPath, toPath, log):
    shutil.copy2(CombPath(fromPath, file), CombPath(toPath, file))
    log.debug('COPY ' + CombPath(fromPath, file) + " " + CombPath(toPath, file))

# ファイルのリネーム
def RenameFile(fromPath, fromFile, toPAth, toFile, log):
    os.rename(CombPath(fromPath, fromFile), CombPath(toPAth, toFile))
    log.debug('RENAME ' + CombPath(toPAth, toFile) + " " + CombPath(fromPath, fromFile))

# ディレクトリ削除
def DeleteDir(path, log):
    shutil.rmtree(path)
    log.debug('DELETE ' + path)

# ファイル削除
def DeleteFile(path, file, log):
    os.remove(CombPath(path,file))
    log.debug('DELETE ' + CombPath(path,file))

# DFからCSVを作成する
def CreateCsvFromDf(df, path, file, log):
    df = df.sort_index()
    df.to_csv(CombPath(path, file))
    log.debug('CREATE ' + CombPath(path, file))

# リストからCSVを作成する
def CreateCsvFromList(df_list, index_list, col_list, filename_list, path, log):
    df = pd.DataFrame(df_list)
    df.index = index_list
    df.columns = col_list
    outputfile = CreateFileName(filename_list,'.csv')
    CreateCsvFromDf(df, path, outputfile, log)

# CSVを上書きする
def UpdateCsv(df, path, filename_list, log):
    outputfile = CreateFileName(filename_list, '.csv')
    CheckCombFile(path, outputfile)
    df = df.sort_index()
    df.to_csv(CombPath(path, outputfile))
    ChmodFile(CombPath(path, outputfile))
    log.debug('UPDATE ' + CombPath(path, outputfile))

# ファイルの拡張子チェック
def SearchFileFromExt(file, ext):
    file_name, file_ext = os.path.splitext(file)
    if file_ext != ext:
        return ""
    return file_name