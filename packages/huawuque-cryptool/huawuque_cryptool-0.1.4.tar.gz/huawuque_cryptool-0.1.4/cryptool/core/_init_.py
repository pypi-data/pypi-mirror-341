# core/__init__.py 
"""
密码学核心模块
包含对称加密、非对称加密等实现
"""
from .app import CryptoCore
from .symmetric import AESHandler#,SM4Handler
from .asymmetric import RSAHandler
from .hashing import SHA256Handler
from .hybrid import HybridHandler
from .key_management import KeyManager
from dotenv import load_dotenv
load_dotenv()

__version__ = "1.0.0"
__all__ = [
    "AESHandler", "CryptoCore", 
    "RSAHandler", "SHA256Handler",
    "HybridHandler", "KeyManager"
]


#__all__ = ["AESHandler", "SM4Handler", "RSAHandler", "SHA256Handler"]#, "generate_random_iv"