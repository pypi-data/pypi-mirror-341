
# -*- codeing = utf-8 -*-
# @Name：hhMysql
# @Version：2.0.0
# @Author：立树
# @CreateTime：2025-04-08 23:45
# @UpdateTime：2025-04-15 15:43

import pymysql
from . import hhJson
from .hhConfig import hhConfig
from .hhResult import Result
from .hhCrypto import Crypto
from typing import Dict, List, Tuple, Union, Optional, Any

class Mysql():
    """
    基于 PyMySQL 封装的 MySQL 操作库
    提供简单易用的数据库操作接口
    """
    
    def __init__(self, host: str = "", port: int = None, username: str = "", password: str = "", database: str = "", charset: str = ""):
        """
        初始化 MySQL 连接参数
        
        参数:
            host: MySQL 服务器地址
            port: MySQL 服务器端口
            username: 用户名
            password: 密码
            database: 数据库名
            charset: 字符集
        """
        # 读取配置文件
        if hhConfig.mysqlConfig["path"] != "" and hhConfig.mysqlConfig["enable"] is True:
            hhMysqlConfig = hhJson.read(hhConfig.mysqlConfig["path"]).data or {}
            host = host or hhMysqlConfig.get("host")
            port = port or hhMysqlConfig.get("port")
            username = username or hhMysqlConfig.get("username")
            password = password or hhMysqlConfig.get("password")
            database = database or hhMysqlConfig.get("database")
            charset = charset or hhMysqlConfig.get("charset")
        # 密码加密
        if hhConfig.mysqlConfig["crypto"] is True:
            crypto = Crypto("hhdb")
            password = crypto.aesDecrypt(password).data
        # 配置参数
        self.config = {
            "host": host,
            "port": port,
            "user": username,
            "password": password,
            "database": database,
            "charset": charset or "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": True
        }
        self.isConnectSuccess = None
        self.connection = None
        self.cursor = None
    
    # 连接数据库
    def connect(self):
        result = Result().initMethod()
        try:
            self.connection = pymysql.connect(**self.config)
            self.cursor = self.connection.cursor()
            self.isConnectSuccess = True
            return result.setState(True).setMsg("数据库连接成功").print("info")
        except Exception as err:
            self.isConnectSuccess = False
            return result.setState(False).setMsg(f"数据库连接失败: {str(err)}").print("error")
    
    # 关闭数据库连接
    def close(self) -> None:
        result = Result().initMethod()
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        return result.setState(True).setMsg("关闭数据库连接").print("info")
    
    def __enter__(self):
        """
        支持 with 语句
        """
        # 连接数据库
        self.connect()
        # 开始事务
        self.begin()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出 with 语句块时自动关闭连接
        """
        # 关闭数据库连接
        self.close()
    
    def execute(self, sql: str, params: Union[tuple, dict, None] = None):
        """
        执行 SQL 语句
        
        参数:
            sql: SQL 语句
            params: SQL 参数
        """
        result = Result().initMethod().setState(True)
        try:
            # with 模式，自动调用 connect() 连接数据库失败
            if self.isConnectSuccess is False:
                return result.setState(False).setMsg("数据库连接失败")
            # 非 with 模式，此前并未调用 connect() 连接数据库
            if not self.connection or self.connection.open is False:
                res = self.connect()
                if res.state is False:
                    return result.setState(False).setMsg(res.msg)
            # 执行 SQL
            result.sql = sql
            result.sql_params = params
            result.affected_rows = self.cursor.execute(sql, params)
            result.rowcount = self.cursor.rowcount
            result.data = None
            return result.setState(True).setMsg("SQL 执行成功").print("info")
        except Exception as err:
            return result.setState(False).setMsg(f"SQL 执行错误: {str(err)}, SQL: {sql}, 参数: {params}").print("error")
    
    def executemany(self, sql: str, params: List[Union[tuple, dict]]):
        """
        批量执行 SQL 语句
        
        参数:
            sql: SQL 语句
            params: 参数列表
        """
        result = Result().initMethod().setState(True)
        try:
            # with 模式，自动调用 connect() 连接数据库失败
            if self.isConnectSuccess is False:
                return result.setState(False).setMsg("数据库连接失败")
            # 非 with 模式，此前并未调用 connect() 连接数据库
            if not self.connection or self.connection.open is False:
                res = self.connect()
                if res.state is False:
                    return result.setState(False).setMsg(res.msg)
            # 执行 SQL
            result.sql = sql
            result.sql_params = params
            result.affected_rows = self.cursor.executemany(sql, params)
            result.data = None
            return result.setState(True).setMsg("SQL 执行成功").print("info")
        except Exception as err:
            return result.setState(False).setMsg(f"批量 SQL 执行错误: {str(err)}, SQL: {sql}, 参数: {params}").print("error")
    
    def query(self, sql: str, params: Union[tuple, dict, None] = None):
        """
        执行查询 SQL 语句
        
        参数:
            sql: SQL 语句
            params: SQL 参数
            
        返回值:
            List[Dict]: 查询结果列表
        """
        result = Result().initMethod()
        try:
            res = self.execute(sql, params)
            if res.state is True:
                res.method = result.method
                res.data = self.cursor.fetchall()
                return res.setMsg("查询成功").print("info")
            else:
                return result.setState(False).setMsg(res.msg).print("error")
        except Exception as err:
            return result.setState(False).setMsg(f"查询错误: {str(err)}, SQL: {sql}, 参数: {params}").print("error")
    
    def query_one(self, sql: str, params: Union[tuple, dict, None] = None):
        """
        查询单条记录
        
        参数:
            sql: SQL 语句
            params: SQL 参数
            
        返回值:
            Optional[Dict]: 查询结果，没有结果时返回 None
        """
        result = Result().initMethod()
        try:
            res = self.execute(sql, params)
            if res.state is True:
                res.method = result.method
                res.data = self.cursor.fetchone()
                return res.setMsg("查询成功").print("info")
            else:
                return result.setState(False).setMsg(res.msg).print("error")
        except Exception as err:
            return result.setState(False).setMsg(f"查询单条记录错误: {str(err)}, SQL: {sql}, 参数: {params}").print("error")
    
    def insert(self, table: str = "", data: Dict = {}):
        """
        插入数据
        
        参数:
            table: 表名
            data: 要插入的数据字典
        """
        result = Result().initMethod()
        try:
            fields = ",".join(f"`{k}`" for k in data.keys())
            placeholders = ",".join(["%s"] * len(data))
            values = list(data.values())
            
            sql = f"INSERT INTO `{table}` ({fields}) VALUES ({placeholders})"
            
            res = self.execute(sql, values)
            if res.state is True:
                res.method = result.method
                res.lastrowid = self.cursor.lastrowid
                return res.setMsg("插入成功").print("info")
            else:
                return result.setState(False).setMsg(res.msg).print("error")
        except Exception as err:
            return result.setState(False).setMsg(f"插入数据错误: {str(err)}, 表: {table}, 数据: {data}").print("error")
    
    def insert_many(self, table: str = "", data_list: List[Dict] = []):
        """
        批量插入数据
        
        参数:
            table: 表名
            data_list: 要插入的数据字典列表
        """
        result = Result().initMethod()
        try:
            fields = ",".join(f"`{k}`" for k in data_list[0].keys())
            placeholders = ",".join(["%s"] * len(data_list[0]))
            
            sql = f"INSERT INTO `{table}` ({fields}) VALUES ({placeholders})"
            values_list = [list(data.values()) for data in data_list]

            res = self.executemany(sql, values_list)
            if res.state is True:
                res.method = result.method
                return res.setMsg("批量插入成功").print("info")
            else:
                return result.setState(False).setMsg(res.msg).print("error")
        except Exception as err:
            return result.setState(False).setMsg(f"批量插入数据错误: {str(err)}, 表: {table}, 数据: {data_list}").print("error")
    
    def update(self, table: str = "", data: Dict = {}, condition: str = "", params: Union[tuple, list, None] = None):
        """
        更新数据
        
        参数:
            table: 表名
            data: 要更新的数据字典
            condition: 条件语句，如 "id = %s"
            params: 条件参数
        """
        result = Result().initMethod()
        try:
            set_clause = ", ".join([f"`{k}` = %s" for k in data.keys()])
            values = list(data.values())
            
            sql = f"UPDATE `{table}` SET {set_clause} WHERE {condition}"
            
            if params:
                if isinstance(params, (list, tuple)):
                    values.extend(params)
                else:
                    values.append(params)
            
            res = self.execute(sql, values)
            if res.state is True:
                res.method = result.method
                return res.setMsg("更新成功").print("info")
            else:
                return result.setState(False).setMsg(res.msg).print("error")
        except Exception as err:
            return result.setState(False).setMsg(f"更新数据错误: {str(err)}, 表: {table}, 数据: {data}, 条件: {condition}, 参数: {params}").print("error")
    
    def delete(self, table: str = "", condition: str = "", params: Union[tuple, list, None] = None):
        """
        删除数据
        
        参数:
            table: 表名
            condition: 条件语句，如 "id = %s"
            params: 条件参数
        """
        result = Result().initMethod()
        try:
            sql = f"DELETE FROM `{table}` WHERE {condition}"
            res = self.execute(sql, params)
            if res.state is True:
                res.method = result.method
                return res.setMsg("删除成功").print("info")
            else:
                return result.setState(False).setMsg(res.msg).print("error")
        except Exception as err:
            return result.setState(False).setMsg(f"删除数据错误: {str(err)}, 表: {table}, 条件: {condition}, 参数: {params}").print("error")
    
    def begin(self) -> None:
        """
        开始事务
        """
        result = Result().initMethod()
        if not self.connection or self.connection.open is False:
            self.connect()
        self.connection.begin()
        print(f"{result.method} - 开始事务")
    
    def commit(self) -> None:
        """
        提交事务
        """
        result = Result().initMethod()
        if self.connection and self.connection.open:
            self.connection.commit()
            print(f"{result.method} - 提交事务")
    
    def rollback(self) -> None:
        """
        回滚事务
        """
        result = Result().initMethod()
        if self.connection and self.connection.open:
            self.connection.rollback()
            print(f"{result.method} - 回滚事务")
    
    def table_exists(self, table: str = ""):
        """
        检查表是否存在
        
        参数:
            table: 表名
        """
        res = self.execute("SHOW TABLES LIKE %s", table)
        if res.affected_rows:
            return Result().initMethod().setState(True).setMsg(f"数据表 {self.config['database']}.{table} 存在").print("info")
        else:
            return Result().initMethod().setState(False).setMsg(f"数据表 {self.config['database']}.{table} 不存在").print("error")
    
    def getTableColumns(self, table: str = ""):
        """
        获取表的列信息
        
        参数:
            table: 表名
        """
        result = Result().initMethod()
        # 检查表是否存在
        res = self.table_exists(table)
        if not res.state:
            res.method = result.method
            return Result().initMethod().setState(False).setData([]).setMsg(res.msg).print("error")
        # 获取表的列信息
        res = self.query(f"SHOW COLUMNS FROM `{table}`")
        if len(res.data):
            return result.setState(True).setData(res.data).setMsg(f"获取数据表 {self.config['database']}.{table} 列信息成功").print("info")
        else:
            return result.setState(False).setData([]).setMsg(f"获取数据表 {self.config['database']}.{table} 列信息失败").print("error")
    
    def getTableCount(self, table: str = ""):
        """
        获取表统计记录数
        
        参数:
            table: 表名
        """
        # 检查表是否存在
        res = self.table_exists(table)
        if not res.state:
            return Result().initMethod().setState(False).setData(0).setMsg(res.msg).print("error")
        
        # 获取表统计记录数
        res = self.query_one(f"SELECT COUNT(*) as count FROM `{table}`")
        result = Result().initMethod()
        result.setState(True)
        result.setData(res.data["count"] or 0)
        result.setMsg(f"获取数据表 {self.config['database']}.{table} 统计记录数成功")
        return result.print("info")
