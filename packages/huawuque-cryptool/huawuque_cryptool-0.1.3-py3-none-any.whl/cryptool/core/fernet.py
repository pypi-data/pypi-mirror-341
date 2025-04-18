import base64
import os
from cryptography.fernet import Fernet as CryptographyFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Fernet:
    def __init__(self, key: bytes):
        """
        初始化Fernet加密器
        :param key: 加密密钥
        """
        self.key = key
        self.fernet = CryptographyFernet(self.key)

    def encrypt(self, data: bytes) -> bytes:
        """
        加密数据
        :param data: 要加密的数据
        :return: 加密后的数据
        """
        return self.fernet.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """
        解密数据
        :param data: 要解密的数据
        :return: 解密后的数据
        """
        return self.fernet.decrypt(data)

    @staticmethod
    def generate_key() -> bytes:
        """
        生成新的Fernet密钥
        :return: 新的密钥
        """
        return CryptographyFernet.generate_key()

    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> bytes:
        """
        从密码派生密钥
        :param password: 密码
        :param salt: 盐值（可选）
        :return: 派生的密钥
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key