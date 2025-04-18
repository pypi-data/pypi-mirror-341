from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from .key_management import KeyManager
from typing import Union, Tuple
import os
import logging

logger = logging.getLogger(__name__)

class AESHandler:
    def __init__(self, key_manager: KeyManager):
        self.key_manager = key_manager
    
    def encrypt(self, data: Union[str, bytes], key: bytes, block_size: int = 4096) -> Tuple[bytes, bytes, bytes]:
        """
        AES加密
        
        Args:
            data: 要加密的数据
            key: 加密密钥
            block_size: 分块大小，默认4KB
            
        Returns:
            (encrypted_data, iv, tag) 三元组
        """
        try:
            # 如果数据是字符串，转换为字节
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # 生成随机IV
            iv = get_random_bytes(16)
            
            # 创建AES加密器
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # 加密数据 - 如果数据大于分块大小，则分块处理
            if len(data) > block_size:
                encrypted_data = b''
                for i in range(0, len(data), block_size):
                    chunk = data[i:i+block_size]
                    # 对每个块进行填充
                    if i + block_size >= len(data):  # 最后一块
                        padded_chunk = pad(chunk, AES.block_size)
                    else:  # 非最后一块，不需要填充
                        padded_chunk = chunk.ljust((len(chunk) // AES.block_size + 1) * AES.block_size, b'\0')
                    encrypted_chunk = cipher.encrypt(padded_chunk)
                    encrypted_data += encrypted_chunk
            else:
                # 小数据直接加密
                padded_data = pad(data, AES.block_size)
                encrypted_data = cipher.encrypt(padded_data)
            
            return encrypted_data, iv, b''  # 返回加密数据、IV和空tag（CBC模式不需要tag）
        except Exception as e:
            logger.error(f"AES加密失败: {e}")
            raise RuntimeError(f"AES加密失败: {str(e)}")
    
    def decrypt(self, encrypted_data: bytes, key: bytes, iv: bytes, tag: bytes = b'', block_size: int = 4096) -> bytes:
        """
        AES解密
        
        Args:
            encrypted_data: 加密数据
            key: 解密密钥
            iv: 初始化向量
            tag: 认证标签(CBC模式未使用)
            block_size: 分块大小，默认4KB
            
        Returns:
            解密后的原始数据
        """
        try:
            # 创建AES解密器
            cipher = AES.new(key, AES.MODE_CBC, iv)
            
            # 解密数据 - 如果加密数据大于分块大小，则分块处理
            if len(encrypted_data) > block_size:
                decrypted_data = b''
                num_blocks = (len(encrypted_data) + block_size - 1) // block_size
                
                for i in range(num_blocks):
                    start = i * block_size
                    end = min((i + 1) * block_size, len(encrypted_data))
                    chunk = encrypted_data[start:end]
                    
                    decrypted_chunk = cipher.decrypt(chunk)
                    
                    # 只对最后一块进行去填充
                    if i == num_blocks - 1:
                        try:
                            decrypted_chunk = unpad(decrypted_chunk, AES.block_size)
                        except Exception as e:
                            logger.warning(f"去填充失败，可能是分块大小不合适: {e}")
                    
                    decrypted_data += decrypted_chunk
                
                return decrypted_data
            else:
                # 小数据直接解密
                decrypted_data = cipher.decrypt(encrypted_data)
                return unpad(decrypted_data, AES.block_size)
        except Exception as e:
            logger.error(f"AES解密失败: {e}")
            raise RuntimeError(f"AES解密失败: {str(e)}")
    
    def encrypt_file(self, input_file: str, output_file: str, key_id: str, chunk_size: int = 1024*1024) -> None:
        """AES分块加密文件"""
        try:
            # 获取密钥
            key_data, algorithm = self.key_manager.get_key(key_id)
            if not key_data:
                raise ValueError(f"未找到密钥: {key_id}")
            
            # 生成随机IV
            iv = get_random_bytes(16)
            
            # 创建AES加密器
            cipher = AES.new(key_data, AES.MODE_CBC, iv)
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                # 写入IV
                f_out.write(iv)
                
                # 分块读取和加密
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    
                    # 对最后一个块进行填充
                    if len(chunk) < chunk_size:
                        padded_chunk = pad(chunk, AES.block_size)
                    else:
                        padded_chunk = chunk
                    
                    # 加密块
                    encrypted_chunk = cipher.encrypt(padded_chunk)
                    f_out.write(encrypted_chunk)
        except Exception as e:
            raise RuntimeError(f"AES文件加密失败: {str(e)}")
    
    def decrypt_file(self, input_file: str, output_file: str, key_id: str, chunk_size: int = 1024*1024) -> None:
        """AES分块解密文件"""
        try:
            # 获取密钥
            key_data, algorithm = self.key_manager.get_key(key_id)
            if not key_data:
                raise ValueError(f"未找到密钥: {key_id}")
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                # 读取IV
                iv = f_in.read(16)
                
                # 创建AES解密器
                cipher = AES.new(key_data, AES.MODE_CBC, iv)
                
                # 分块读取和解密
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    
                    # 解密块
                    decrypted_chunk = cipher.decrypt(chunk)
                    
                    # 如果是最后一个块，去除填充
                    if len(chunk) < chunk_size:
                        decrypted_chunk = unpad(decrypted_chunk, AES.block_size)
                    
                    f_out.write(decrypted_chunk)
        except Exception as e:
            raise RuntimeError(f"AES文件解密失败: {str(e)}")