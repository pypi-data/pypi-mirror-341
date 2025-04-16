
# -*- codeing = utf-8 -*-
# @Name：hhMock
# @Version：1.0.0
# @Author：立树
# @Document：https://faker.readthedocs.io/
# @CreateTime：2025-04-09 13:43
# @UpdateTime：2025-04-12 00:38

"""
功能：
- setLanguage 设置语言功能
- name 生成随机姓名功能
- email 生成随机邮箱功能
- phone 生成随机手机号功能
- gender 生成随机性别功能
- date 生成随机日期时间功能
- birthday 生成随机出生日期功能
- timestamp 生成随机时间戳功能
- uuid 生成随机 UUID 功能
- image 生成随机图片 URL 功能
- word 生成随机单词功能
- sentence 生成随机句子功能
- paragraph 生成随机段落功能
"""

import re
import random
import urllib.parse
from faker import Faker
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Union, Optional, Any

class Mock():
    """
    基于 Faker 封装的数据模拟库，提供简单易用的 Mock 操作接口
    """

    # Faker 对象
    Faker = Faker
    
    # 构造函数
    def __init__(self, lang: str = "cn"):
        """
        初始化 Mock 对象
        
        参数:
            lang: 语言
        """
        language = self.__transLanguage(lang)
        self.language = language
        self.faker = Faker(language)

    # 当访问不存在的方法或属性时，直接在 self.faker 实例上调用
    def __getattr__(self, name: str) -> Any:
        """
        当访问不存在的方法或属性时，直接在 self.faker 实例上调用
        
        参数:
            name: 方法或属性名称
        
        返回值:
            Any: self.faker 实例对应的方法或属性
        
        示例:
            hhMock.phone_number() 会转发到 hhMock.faker.phone_number()
        """
        if hasattr(self.faker, name):
            return getattr(self.faker, name)
        else:
            raise AttributeError(f"'{name}' 属性/方法不存在")

    # 转换语言（内部函数）
    def __transLanguage(self, lang: str = "") -> str:
        if lang:
            Language = {
                "cn": "zh_CN",
                "zh": "zh_CN",
                "en": "en_US",
            }
            return Language.get(lang, lang)
        else:
            return self.language
    
    # 设置语言
    def setLanguage(self, lang: str = ""):
        """
        设置语言
        
        参数:
            lang: 语言
        """
        language = self.__transLanguage(lang)
        self.language = language
        self.faker = Faker(language)
    
    # 生成随机姓名
    def name(self, gender: str = "", lang: str = "") -> str:
        """
        生成随机姓名
        
        参数:
            gender: 性别
            lang: 语言
        
        返回值:
            str: 随机姓名
        """

        language = self.__transLanguage(lang)
        faker = Faker(language) if self.language != language else self.faker
        
        if gender == "男":
            return faker.name_male()
        elif gender == "女":
            return faker.name_female()
        else:
            return faker.name()
    
    # 生成随机邮箱
    def email(self, domain: Union[tuple, list, str] = None) -> str:
        """
        生成随机邮箱

        参数:
            domain: 邮箱域名
        
        返回值:
            str: 随机邮箱
        """
        # 邮箱域名池
        EmailDomains = (
            # 国内
            "qq.com",
            "163.com",
            "126.com",
            "sina.com",
            # 国外
            # "gmail.com",
            # "outlook.com",
            # "hotmail.com",
            # "yahoo.com",
            # "icloud.com",
        )

        # 参数处理
        if isinstance(domain, (list, tuple)):
            domain = random.choice(domain)
        elif isinstance(domain, str):
            domain = domain
        else:
            domain = random.choice(EmailDomains)
        
        return self.faker.email(domain = domain)
    
    # 生成随机手机号
    def phone(self) -> str:
        """
        生成随机手机号
        
        返回值:
            str: 随机手机号
        """
        # 获取国家区号
        # print(self.faker.country_calling_code())
        return self.faker.phone_number()
    
    # 生成随机性别
    def gender(self, enums: Union[tuple, list, str] = None) -> str:
        """
        生成随机性别

        参数:
            enums: 性别枚举
        
        返回值:
            str: 随机性别
        """
        # 参数处理
        if isinstance(enums, (list, tuple)):
            genders = enums
        elif isinstance(enums, str):
            genders = (enums,)
        else:
            genders = ("男", "女")
        
        # return self.faker.profile()["sex"]
        return self.faker.random_element(elements = genders)
    
    # 日期字符串转换为日期（内部函数）
    def __transDatestrToDatetime(self, date_str: str) -> Union[datetime, str]:
        if not isinstance(date_str, str):
            return date_str

        # 定义正则表达式模式和对应的格式字符串
        patterns = [
            # 完整日期时间: 2000-01-01 00:00:00
            (r"^\d{4}[-/]\d{1,2}[-/]\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$",
            lambda s: s.replace("/", "-"),
            "%Y-%m-%d %H:%M:%S"),
            
            # 日期时间(无秒): 2000-01-01 00:00
            (r"^\d{4}[-/]\d{1,2}[-/]\d{1,2} \d{1,2}:\d{1,2}$",
            lambda s: s.replace("/", "-"),
            "%Y-%m-%d %H:%M"),
            
            # 仅日期: 2000-01-01
            (r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}$",
            lambda s: s.replace("/", "-"),
            "%Y-%m-%d"),
            
            # 年月: 2000-01
            (r"^\d{4}[-/]\d{1,2}$",
            lambda s: s.replace("/", "-"),
            "%Y-%m"),
            
            # 仅年份: 2000
            (r"^\d{4}$",
            lambda s: s,
            "%Y"),
        ]
        
        # 尝试匹配所有模式
        for pattern, normalizer, format_str in patterns:
            if re.match(pattern, date_str):
                normalized_str = normalizer(date_str)
                try:
                    return datetime.strptime(normalized_str, format_str)
                except ValueError:
                    continue
        
        # 如果仍然无法解析，返回原始字符串
        return date_str
    
    # 生成随机日期时间
    def date(self, pattern: str = None, range: Union[list, tuple, str] = None, start = None, end = None, returnType: str = "str") -> Union[str, datetime]:
        """
        生成随机日期时间
        
        参数:
            pattern: 日期格式，支持 "YYYY-MM-DD hh:mm:ss"
            range: 日期范围，支持 "now" | "today" | "this_month" | "this_year" | list | tuple
            start: 开始日期，支持 date | datetime | datetime string | timedelta | timedelta string | int
            end: 结束日期，支持 date | datetime | datetime string | timedelta | timedelta string | int
            returnType: 返回类型，支持 "str" 或 "datetime"
        
        返回值:
            str: 随机日期时间
            datetime: 随机日期时间
        """

        # 时间偏移字符串（timedelta string）
        # 
        # [ 基本时间单位 ]
        # | 符号 | 时间单位        | 示例  | 说明       |
        # |-----|----------------|------|------------|
        # | y   | 年(years)      | +1y   | 1年后      |
        # | M   | 月(months)     | -2M   | 2个月前    |
        # | w   | 周(weeks)      | +4w   | 4周后      |
        # | d   | 天(days)       | -10d  | 10天前     |
        # | h   | 小时(hours)    | +12h  | 12小时后    |
        # | m   | 分钟(minutes)  | -30m  | 30分钟前    |
        # | s   | 秒(seconds)    | +45s  | 45秒后     |
        # 
        # [ 复合格式 ]
        # | 示例         | 说明             |
        # |-------------|------------------|
        # | +1y2M       | 1年零2个月后      |
        # | -3d12h      | 3天12小时前       |
        # | +2w3d       | 2周零3天后        |
        # | -1y6M15d    | 1年6个月15天前    |

        # 日期格式
        if pattern:
            pattern = (pattern
                .replace("YYYY", "%Y")
                .replace("YY", "%y")
                .replace("MM", "%m")
                .replace("DD", "%d")
                .replace("hh", "%H")
                .replace("mm", "%M")
                .replace("ss", "%S")
            )
        else:
            pattern = "%Y-%m-%d %H:%M:%S"
        
        # 日期范围
        if range == "now":
            start = "now"
            end = "now"
        elif range == "today":
            now = datetime.now()
            start = datetime(now.year, now.month, now.day, 0, 0, 0)
            end = datetime(now.year, now.month, now.day, 23, 59, 59)
        elif range == "this_month":
            now = datetime.now()
            start = datetime(now.year, now.month, 1, 0, 0, 0)
            end = datetime(now.year, now.month + 1, 1, 0, 0, 0) - timedelta(seconds = 1)
        elif range == "this_year":
            now = datetime.now()
            start = datetime(now.year, 1, 1, 0, 0, 0)
            end = datetime(now.year + 1, 1, 1, 0, 0, 0) - timedelta(seconds = 1)
        elif isinstance(range, (list, tuple)) and len(range) == 2:
            start = start or range[0] or "-30y"
            end = end or range[1] or "now"
            start = self.__transDatestrToDatetime(start)
            end = self.__transDatestrToDatetime(end)
        else:
            start = self.__transDatestrToDatetime(start) or "-30y"
            end = self.__transDatestrToDatetime(end) or "now"
        
        # 生成随机日期
        date = self.faker.date_time_between(start_date = start, end_date = end)

        # 返回类型
        if returnType == "datetime":
            return date
        else:
            return date.strftime(pattern)
    
    # 生成随机出生日期
    def birthday(self, minAge: int = None, maxAge: int = None, range: Union[list, tuple] = None, pattern: str = None, returnType: str = "str") -> Union[str, datetime.date]:
        """
        生成随机出生日期

        参数:
            minAge: 最小年龄
            maxAge: 最大年龄
            range: 日期范围，支持 list | tuple
            pattern: 日期格式
            returnType: 返回类型，支持 "str" 或 "datetime"

        返回值:
            str: 随机出生日期
            datetime: 随机出生日期
        """

        # 日期格式
        if pattern:
            pattern = (pattern
                .replace("YYYY", "%Y")
                .replace("YY", "%y")
                .replace("MM", "%m")
                .replace("DD", "%d")
                .replace("hh", "%H")
                .replace("mm", "%M")
                .replace("ss", "%S")
            )
        else:
            pattern = "%Y-%m-%d"
        
        # 年龄范围
        if isinstance(range, (list, tuple)) and len(range) == 2:
            minAge = minAge or range[0] or 0
            maxAge = maxAge or range[1] or 115
        else:
            minAge = minAge or 0
            maxAge = maxAge or 115
        
        # 生成随机出生日期
        birthday = self.faker.date_of_birth(minimum_age = minAge, maximum_age = maxAge, tzinfo = None)

        # 返回类型
        if returnType == "datetime":
            return birthday
        else:
            return birthday.strftime(pattern)
    
    # 生成随机时间戳
    def timestamp(self, start = None, end = None, range: Union[list, tuple, str] = None, returnType: str = "int") -> Union[int, float]:
        """
        生成随机时间戳
        
        参数:
            returnType: 返回类型，支持 "int" 或 "float"
            range: 日期范围，支持 "now" | "today" | "this_month" | "this_year" | list | tuple
            start: 开始日期，支持 date | datetime | datetime string | timedelta | timedelta string | int
            end: 结束日期，支持 date | datetime | datetime string | timedelta | timedelta string | int
        
        返回值:
            int: 整数格式的时间戳（秒）
            float: 浮点数格式的时间戳（秒.毫秒）
        """
        
        # 生成随机日期
        date = self.date(range = range, start = start, end = end, returnType = "datetime")
        
        # 转换为时间戳
        timestamp = date.timestamp()
        
        # 返回类型
        if returnType == "float":
            return timestamp
        else:
            return int(timestamp)

    # 生成随机 UUID
    def uuid(self) -> str:
        """
        生成随机 UUID

        返回值:
            str: 随机 UUID
        """
        return self.faker.uuid4()

    # 生成随机图片 URL
    def image(self, size: str = "300x200", text: str = "", textColor: str = "fff", bgColor: str = "000", ext: str = "png") -> str:
        """
        生成随机图片URL
        
        参数:
            size: 图片尺寸，格式为 "宽度x高度"，例如 "300x200"
            text: 图片上的文字
            textColor: 文字颜色，十六进制格式，不含 "#" 前缀
            bgColor: 图片背景色，十六进制格式，不含 "#" 前缀
            ext: 图片扩展名，可选 png、gif、jpg、jpeg
        
        返回值:
            str: 生成的图片 URL，文字部分经过 URL 编码
        
        示例:
            hhMock.image(size="500x300", text="Hello World", textColor="fff", bgColor="000", ext="jpg")
            返回: "https://dummyimage.com/500x300/000/fff.jpg&text=Hello+World"
        """
        
        # 尺寸格式：数字x数字
        size_pattern = r"^\d+x\d+$"
        if not size or not isinstance(size, str) or not re.match(size_pattern, size):
            size = "300x200"
        
        # 颜色格式：3位或6位十六进制数字
        color_pattern = r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"
        if not textColor or not isinstance(textColor, str) or not re.match(color_pattern, textColor):
            textColor = "fff"
        
        if not bgColor or not isinstance(bgColor, str) or not re.match(color_pattern, bgColor):
            bgColor = "000"
        
        # 移除颜色中可能存在的 # 前缀
        textColor = textColor.replace("#", "")
        bgColor = bgColor.replace("#", "")
        
        # 扩展名格式：png、gif、jpg、jpeg
        valid_extensions = ["png", "gif", "jpg", "jpeg"]
        if not ext or not isinstance(ext, str) or ext.lower() not in valid_extensions:
            ext = "png"
        
        # 构建基础 URL
        base_url = f"https://dummyimage.com/{size}/{bgColor}/{textColor}.{ext}"
        
        # 如果有文字，进行处理后添加到 URL
        if text and isinstance(text, str):
            # 先将空格替换为加号，然后对其他特殊字符进行编码
            text_with_plus = text.replace(" ", "+")
            
            # 对除了加号外的特殊字符进行 URL 编码，使用 urllib 编码后再替换回加号
            encoded_text = urllib.parse.quote(text_with_plus).replace("%2B", "+")
            
            # 添加到 URL
            base_url += f"&text={encoded_text}"
        
        return base_url

    # 生成随机单词
    def word(self, words: Union[list, tuple] = None, lang: str = "") -> str:
        """
        生成随机单词
        
        参数:
            words: 单词列表，如果提供，将从此列表中随机选择
            lang: 语言，支持 "cn" | "zh" | "en" 等
        
        返回值:
            str: 随机单词
        
        示例:
            hhMock.word()
            返回: "风景"
            
            hhMock.word(lang="en")
            返回: "beautiful"
            
            hhMock.word(words=["苹果", "香蕉", "橙子"])
            返回: "香蕉"
        """
        
        # 如果提供了扩展单词列表，则从列表中随机选择一个
        if words and isinstance(words, (list, tuple)) and len(words) > 0:
            return self.faker.random_element(elements = words)
        
        # 如果指定了语言，创建对应语言的 Faker 实例
        if lang:
            language = self.__transLanguage(lang)
            faker = Faker(language) if self.language != language else self.faker
        else:
            faker = self.faker
        
        # 生成随机单词
        return faker.word()

    # 生成随机句子
    def sentence(self, minNum: int = None, maxNum: int = None, words: Union[list, tuple] = None, lang: str = "") -> str:
        """
        生成随机句子
        
        参数:
            minNum: 最小文字数量
            maxNum: 最大文字数量
            words: 单词列表，如果提供，将从此列表中随机选择单词构建句子
            lang: 语言，支持 "cn" | "zh" | "en" 等
        
        返回值:
            str: 随机句子
        
        示例:
            hhMock.sentence()
            返回: "我喜欢这个美丽的风景。"
            
            hhMock.sentence(minNum=15, maxNum=20, lang="en")
            返回: "Beautiful day today."
            
            hhMock.sentence(words=["苹果", "香蕉", "橙子", "水果", "新鲜", "甜"])
            返回: "新鲜香蕉苹果水果甜橙子。"
        """
        
        # 语言
        language = self.__transLanguage(lang)
        faker = Faker(language) if self.language != language else self.faker

        # 确保最小字符数和最大字符数有效
        defMinNum = 12
        defMaxNum = 20
        if minNum and maxNum:
            # 最小文字数量 [Y]、最大文字数量 [Y]
            minNum = int(minNum) if isinstance(minNum, (int, float)) and minNum > 0 else defMinNum
            maxNum = int(maxNum) if isinstance(maxNum, (int, float)) and maxNum > 0 else defMaxNum
        elif minNum and not maxNum:
            # 最小文字数量 [Y]、最大文字数量 [N]
            minNum = int(minNum) if isinstance(minNum, (int, float)) and minNum > 0 else defMinNum
            maxNum = minNum
        else:
            # 最小文字数量 [N]、最大文字数量 [N]
            minNum = defMinNum
            maxNum = defMaxNum

        # 确定要生成的单词数量
        minNum = min(minNum, maxNum)
        maxNum = max(minNum, maxNum)
        num = random.randint(minNum, maxNum)
        
        # 如果提供了扩展单词列表，则使用这些单词构建句子
        if words and isinstance(words, (list, tuple)) and len(words) > 0:
            # 从单词列表中随机选择单词
            selected_words = []
            for _ in range(num):
                selected_words.append(faker.random_element(elements=words))
            
            # 根据语言环境添加适当的标点符号
            if language == "zh_CN":
                sentence = "".join(selected_words)[0:num] + "。"
            else:
                sentence = " ".join(selected_words).capitalize()[0:num] + "."
            
            return sentence
        
        # 生成随机单词
        sentence = faker.sentence(nb_words = maxNum, variable_nb_words = False)
        sentence = sentence[0:num-1]
        if language == "zh_CN":
            sentence += "。"
            # 文字过长时，插入逗号
            if num >= 20:
                idx = random.randint(int(num * 0.25), int(num * 0.4))
                sentence = sentence[0:idx] + "，" + sentence[idx + 1:]
        else:
            sentence += "."
        
        return sentence

    # 生成随机段落
    def paragraph(self, minNum: int = None, maxNum: int = None, words: Union[list, tuple] = None, lang: str = "") -> str:
        """
        生成随机段落
        
        参数:
            minNum: 最小句子数量
            maxNum: 最大句子数量
            words: 单词列表，如果提供，将从此列表中随机选择单词构建句子
            lang: 语言，支持 "cn" | "zh" | "en" 等
        
        返回值:
            str: 随机段落
        
        示例:
            hhMock.paragraph()
            返回: "我喜欢这个美丽的风景。今天天气真好。阳光明媚鸟语花香。"
            
            hhMock.paragraph(minNum=2, maxNum=3, lang="en")
            返回: "Beautiful day today. The sun is shining brightly."
            
            hhMock.paragraph(words=["苹果", "香蕉", "橙子", "水果", "新鲜", "甜"])
            返回: "新鲜香蕉苹果水果甜橙子。水果香蕉新鲜甜。苹果橙子甜水果新鲜。"
        """
        
        # 语言
        language = self.__transLanguage(lang)

        # 确保最小句子数和最大句子数有效
        defMinNum = 2
        defMaxNum = 4
        if minNum and maxNum:
            # 最小句子数量 [Y]、最大句子数量 [Y]
            minNum = int(minNum) if isinstance(minNum, (int, float)) and minNum > 0 else defMinNum
            maxNum = int(maxNum) if isinstance(maxNum, (int, float)) and maxNum > 0 else defMaxNum
        elif minNum and not maxNum:
            # 最小句子数量 [Y]、最大句子数量 [N]
            minNum = int(minNum) if isinstance(minNum, (int, float)) and minNum > 0 else defMinNum
            maxNum = minNum
        else:
            # 最小句子数量 [N]、最大句子数量 [N]
            minNum = defMinNum
            maxNum = defMaxNum
        
        # 确定要生成的句子数量
        minNum = min(minNum, maxNum)
        maxNum = max(minNum, maxNum)
        num = random.randint(minNum, maxNum)
        
        # 生成多个句子
        sentences = []
        for _ in range(num):
            sentence = self.sentence(
                minNum = 5 if language == "zh_CN" else 15,
                maxNum = 40 if language == "zh_CN" else 75,
                words = words,
                lang = language
            )
            sentences.append(sentence)
        
        # 根据语言环境组合句子
        if language == "zh_CN":
            # 中文段落不需要额外空格
            paragraph = "".join(sentences)
        else:
            # 英文段落需要空格分隔
            paragraph = " ".join(sentences)
        
        return paragraph

# 实例化 Mock 对象
hhMock = Mock()
