# 哈希计算模块
"""
安全哈希计算模块
支持SHA-256、HMAC、PBKDF2密钥派生等功能
"""

import hmac
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from typing import Union, Tuple
import os

from cryptool.core.key_management import KeyManager

class SHA256Handler:
    def __init__(self, hash_algorithm: str = "SHA256", salt_length: int = 16):
        """支持扩展哈希算法选择"""
        self.hash_module = self._select_hash_module(hash_algorithm)  # 如SHA3_256
        self.salt_length = salt_length

    def _select_hash_module(self, algorithm: str):
        """选择哈希算法模块"""
        if algorithm.upper() == "SHA256":
            return SHA256
        else:
            raise ValueError(f"不支持的哈希算法: {algorithm}")

    def compute_hash(self, data: bytes) -> bytes:
        """
        计算数据的SHA-256哈希值
        :param data: 输入字节数据
        :return: 哈希值字节
        """
        h = self.hash_module.new(data)
        return h.digest()

    def compute_hmac(self, data: bytes, key: bytes) -> bytes:
        """
        计算HMAC-SHA256
        :param data: 原始数据
        :param key: HMAC密钥
        :return: HMAC值字节
        """
        try:
            # 创建HMAC对象
            hmac_obj = hmac.new(key, digestmod='sha256')
            
            # 更新数据
            hmac_obj.update(data)
            
            # 获取HMAC值
            return hmac_obj.digest()
        except Exception as e:
            raise RuntimeError(f"HMAC计算失败: {str(e)}")

    def verify(self, data: bytes, signature: bytes, key: bytes) -> bool:
        """
        验证HMAC签名
        :param data: 原始数据
        :param signature: HMAC签名
        :param key: HMAC密钥
        :return: 验证是否通过
        """
        try:
            # 计算数据的HMAC
            computed_hmac = self.compute_hmac(data, key)
            
            # 比较HMAC值
            return hmac.compare_digest(computed_hmac, signature)
        except Exception as e:
            raise RuntimeError(f"HMAC验证失败: {str(e)}")

    def pbkdf2_derive(self, password: Union[str, bytes], 
                     iterations: int = 100000) -> Tuple[bytes, bytes]:
        """
        使用PBKDF2派生密钥
        :param password: 原始密码（字符串或字节）
        :param iterations: 迭代次数，默认10万次
        :return: (派生密钥, 盐值)
        """
        if isinstance(password, str):
            password = password.encode('utf-8')
        
        salt = get_random_bytes(self.salt_length)
        key = PBKDF2(password, salt, dkLen=32, count=iterations, hmac_hash_module=self.hash_module)
        return key, salt

    def verify_hash(self, data: bytes, target_hash: bytes) -> bool:
        """
        验证哈希值是否匹配
        :param data: 原始数据
        :param target_hash: 要验证的哈希值
        :return: 是否匹配
        """
        return hmac.compare_digest(self.compute_hash(data), target_hash)

    def file_hash(self, file_path: str, block_size: int = 65536) -> bytes:
        """
        计算大文件的SHA-256哈希
        :param file_path: 文件路径
        :param block_size: 分块读取大小
        :return: 文件哈希值
        """
        h = self.hash_module.new()
        with open(file_path, 'rb') as f:
            while True:
                block = f.read(block_size)
                if not block:
                    break
                h.update(block)
        return h.digest()

    @staticmethod
    def generate_random_salt(length: int = 16) -> bytes:
        """生成密码学安全的随机盐值"""
        return os.urandom(length)