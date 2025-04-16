
# -*- codeing = utf-8 -*-
# @Name：hhCrypto
# @Version：1.0.0
# @Author：立树
# @CreateTime：2025-04-15 14:26
# @UpdateTime：2025-04-15 15:35

import hashlib
import base64
from Crypto.Cipher import AES
from .hhResult import Result

class Crypto:
    def __init__(self, crypto_key):
        """
        初始化加密类
        
        参数:
            crypto_key: 加密密钥
        """
        self.crypto_key = crypto_key
        
    def aesEncrypt(self, plaintext):
        """
        AES 加密方法 (CBC, 128)
        
        参数:
            plaintext: 待加密的字符串
        
        返回值:
            加密后的字符串
        """
        result = Result().initMethod()
        try:
            # 将输入文本转换为字节，如果是字符串
            if isinstance(plaintext, str):
                plaintext = plaintext.encode("utf-8")
            
            # 生成密钥和初始化向量
            key = hashlib.md5(self.crypto_key.strip().encode("utf-8")).hexdigest().encode("utf-8")
            iv = key[:16]  # 取前16位作为 IV
            
            # 使用零填充，填充到块大小 (16字节)
            block_size = 16
            padding_length = block_size - (len(plaintext) % block_size)
            if padding_length == 0:
                padding_length = block_size
            padded_data = plaintext + (b"\0" * padding_length)
            
            # 创建 AES-CBC 加密器
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # 加密数据
            ciphertext = cipher.encrypt(padded_data)
            
            # 将加密后的数据进行 base64 编码
            ciphertext = base64.b64encode(ciphertext).decode("utf-8")

            return result.setState(True).setData(ciphertext).setMsg("加密成功").print("info")
        except Exception as err:
            return result.setState(False).setData("").setMsg(f"加密失败: {str(err)}").print("error")
    
    def aesDecrypt(self, ciphertext):
        """
        AES 解密方法 (CBC, 128)
        
        参数:
            ciphertext: 待解密的字符串
        
        返回值:
            解密后的字符串
        """
        result = Result().initMethod()
        try:
            # 对 base64 编码的加密文本进行解码
            ciphertext = base64.b64decode(ciphertext)
            
            # 生成密钥和初始化向量
            key = hashlib.md5(self.crypto_key.strip().encode("utf-8")).hexdigest().encode("utf-8")
            iv = key[:16]  # 取前16位作为 IV
            
            # 创建 AES-CBC 解密器
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # 解密数据
            plaintext = cipher.decrypt(ciphertext)
        
            # 加密时使用零填充，所以我们需要去除末尾的空字节
            plaintext = plaintext.rstrip(b"\0")
            
            # 将解密后的字节转换回字符串
            plaintext = plaintext.decode("utf-8").strip()
            return result.setState(True).setData(plaintext).setMsg("解密成功").print("info")
        except Exception as err:
            return result.setState(False).setData("").setMsg(f"解密失败: {str(err)}").print("error")
