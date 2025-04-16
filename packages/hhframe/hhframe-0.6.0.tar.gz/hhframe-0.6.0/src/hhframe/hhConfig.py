
# -*- codeing = utf-8 -*-
# @Name：hhConfig
# @Version：1.1.0
# @Author：立树
# @CreateTime：2025-04-02 13:50
# @UpdateTime：2025-04-15 15:35

"""
功能：
- setMysqlConfig 设置 Mysql 配置
- setKuaiProxyConfig 设置快代理配置
更新：
- 新增 self.mysqlConfig 配置
- 新增 __findConfigFile 自动查找配置文件功能
"""

import os
import json
from .hhUtils import getAbsolutePath

class Config():
    # 初始化
    def __init__(self):
        # 基础配置
        self.name = "hhframe"
        self.version = "0.6.0"
        self.author = "立树"
        self.mode = "run"
        # self.mode = "debug"

        # Mysql
        self.mysqlConfig = {
            "enable": True,
            "crypto": True,
            "path": ""
        }

        # 快代理
        self.kuaiProxyConfig = {
            "enable": False,
            "path": ""
        }

        # 自动查找配置文件
        self.__findConfigFile()

    # 打印结果
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii = False, indent = 4)
    
    # 自动查找配置文件
    def __findConfigFile(self):
        runCounts = 0
        foundedConfigFiles = 0
        skipDirs = [".venv", "venv", ".git", ".idea", "dist", "build", "__pycache__"]
        for root, dirs, files in os.walk(os.getcwd(), topdown = True):
            runCounts += 1
            # print("root - ", root)
            # print("dirs - ", dirs)
            # print("files - ", files)
            # print("=" * 50, runCounts, foundedConfigFiles)

            if os.path.split(root)[1] in skipDirs:
                dirs.clear()
                files.clear()
                continue
            
            # 过滤无效文件夹
            for dir in dirs:
                if dir in skipDirs:
                    dirs.remove(dir)
            
            # 筛选配置文件
            for file in files:
                # Mysql
                if self.mysqlConfig["path"] == "" and file in ["hhMysqlConfig.json"]:
                    self.mysqlConfig["path"] = os.path.join(root, file)
                    foundedConfigFiles += 1
                # 快代理
                if self.kuaiProxyConfig["path"] == "" and file in ["hhKuaiProxyConfig.json"]:
                    self.kuaiProxyConfig["path"] = os.path.join(root, file)
                    foundedConfigFiles += 1
                # 查找到全部配置文件
                if foundedConfigFiles == 2:
                    return
    
    # 设置 Mysql 配置
    def setMysqlConfig(self, config):
        try:
            if config.get("enable") != None:
                self.mysqlConfig["enable"] = config.get("enable")
            if config.get("crypto") != None:
                self.mysqlConfig["crypto"] = config.get("crypto")
            if config.get("path") != None:
                self.mysqlConfig["path"] = getAbsolutePath(config.get("path"), depth = 2)
        except Exception:
            pass
    
    # 设置快代理配置
    def setKuaiProxyConfig(self, config):
        try:
            if config.get("enable") != None:
                self.kuaiProxyConfig["enable"] = config.get("enable")
            if config.get("path") != None:
                self.kuaiProxyConfig["path"] = getAbsolutePath(config.get("path"), depth = 2)
        except Exception:
            pass

hhConfig = Config()
