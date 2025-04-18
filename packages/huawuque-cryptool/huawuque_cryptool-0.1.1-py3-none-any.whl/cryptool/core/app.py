"""
加密工具应用核心类
"""
import os
import base64
import logging
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import hashes, serialization

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/crypto.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

class CryptoApp:
    """加密工具核心应用类"""
    
    def __init__(self):
        """初始化加密工具"""
        # 确保日志目录存在
        os.makedirs('logs', exist_ok=True)
        # 确保密钥目录存在
        os.makedirs('keys', exist_ok=True)
        
        # 默认AES密钥
        self.aes_key = os.urandom(32)  # 256位密钥
        # 生成默认RSA密钥对
        self._generate_rsa_keys()
        
        logger.info("加密工具初始化完成")
    
    def _generate_rsa_keys(self):
        """生成RSA密钥对"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.rsa_private_key = private_key
        self.rsa_public_key = private_key.public_key()
        logger.info("RSA密钥对生成完成")
    
    def encrypt_aes(self, plaintext):
        """AES加密"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
            
        # 生成随机IV
        iv = os.urandom(16)
        
        # 创建加密器
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # 添加填充
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # 加密
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # 组合IV和密文，并进行Base64编码
        result = base64.b64encode(iv + ciphertext).decode('utf-8')
        
        logger.info(f"AES加密完成，输入长度: {len(plaintext)}，输出长度: {len(result)}")
        return result
    
    def decrypt_aes(self, ciphertext):
        """AES解密"""
        try:
            # Base64解码
            data = base64.b64decode(ciphertext)
            
            # 提取IV和密文
            iv = data[:16]
            actual_ciphertext = data[16:]
            
            # 创建解密器
            cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            
            # 解密
            padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
            
            # 移除填充
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            
            result = plaintext.decode('utf-8')
            logger.info(f"AES解密完成，输入长度: {len(ciphertext)}，输出长度: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"AES解密失败: {str(e)}")
            raise Exception(f"解密失败: {str(e)}")
    
    def encrypt_rsa(self, plaintext):
        """RSA加密"""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
            
        ciphertext = self.rsa_public_key.encrypt(
            plaintext,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        result = base64.b64encode(ciphertext).decode('utf-8')
        logger.info(f"RSA加密完成，输入长度: {len(plaintext)}，输出长度: {len(result)}")
        return result
    
    def decrypt_rsa(self, ciphertext):
        """RSA解密"""
        try:
            # Base64解码
            ciphertext_bytes = base64.b64decode(ciphertext)
            
            plaintext = self.rsa_private_key.decrypt(
                ciphertext_bytes,
                asymmetric_padding.OAEP(
                    mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            result = plaintext.decode('utf-8')
            logger.info(f"RSA解密完成，输入长度: {len(ciphertext)}，输出长度: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"RSA解密失败: {str(e)}")
            raise Exception(f"解密失败: {str(e)}")
    
    def encrypt_hybrid(self, plaintext):
        """混合加密 (RSA + AES)"""
        # 生成一次性AES密钥
        session_key = os.urandom(32)
        
        # 使用RSA加密会话密钥
        encrypted_session_key = self.rsa_public_key.encrypt(
            session_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # 使用会话密钥通过AES加密数据
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
            
        # 生成随机IV
        iv = os.urandom(16)
        
        # 创建加密器
        cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # 添加填充
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # 加密
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # 组合密文包
        encrypted_data = {
            'session_key': base64.b64encode(encrypted_session_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
        }
        
        logger.info(f"混合加密完成，输入长度: {len(plaintext)}")
        return encrypted_data
    
    def decrypt_hybrid(self, encrypted_data):
        """混合解密 (RSA + AES)"""
        try:
            # 解密会话密钥
            encrypted_session_key = base64.b64decode(encrypted_data['session_key'])
            session_key = self.rsa_private_key.decrypt(
                encrypted_session_key,
                asymmetric_padding.OAEP(
                    mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # 解密数据
            iv = base64.b64decode(encrypted_data['iv'])
            ciphertext = base64.b64decode(encrypted_data['ciphertext'])
            
            # 创建解密器
            cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            
            # 解密
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # 移除填充
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            
            result = plaintext.decode('utf-8')
            logger.info(f"混合解密完成，输出长度: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"混合解密失败: {str(e)}")
            raise Exception(f"解密失败: {str(e)}")
    
    def encode_base64(self, data):
        """Base64编码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    
    def decode_base64(self, data):
        """Base64解码"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64decode(data).decode('utf-8') 