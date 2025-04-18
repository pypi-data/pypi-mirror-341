from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from .symmetric import AESHandler
from .asymmetric import RSAHandler
from .hashing import SHA256Handler
from .key_management import KeyManager
import os
from typing import Tuple, Optional, Any, Union
from Crypto.PublicKey.RSA import RsaKey
import logging
from Crypto.PublicKey import RSA

logger = logging.getLogger(__name__)

class HybridHandler:
    def __init__(self, key_manager: KeyManager, aes_handler: AESHandler, rsa_handler: RSAHandler):
        self.key_manager = key_manager
        self.aes_handler = aes_handler
        self.rsa_handler = rsa_handler
        self.hash = SHA256Handler() # SHA256Handler 通常不需要 KeyManager
    #混合加密
    def encrypt(self, plaintext: Union[str, bytes], key_id: str) -> dict:
        """
        混合加密
        :param plaintext: 明文
        :param key_id: 密钥ID
        :return: 包含加密结果的字典
        """
        try:
            # 生成AES密钥
            aes_key = get_random_bytes(32)  # 256-bit key
            
            # 检查key_id是否已经包含'_public'后缀
            rsa_key_id = key_id
            if not key_id.endswith('_public'):
                rsa_key_id = key_id + '_public'
            
            # 使用RSA加密AES密钥
            encrypted_aes_key = self.rsa_handler.encrypt(aes_key, rsa_key_id)
            
            # 使用AES加密明文
            ciphertext, iv, tag = self.aes_handler.encrypt(data=plaintext, key=aes_key)
            
            # 计算HMAC
            hmac_key = get_random_bytes(32)
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            hmac.update(ciphertext)
            hmac_signature = hmac.digest()
            
            # 使用RSA加密HMAC密钥
            encrypted_hmac_key = self.rsa_handler.encrypt(hmac_key, rsa_key_id)
            
            result = {
                'ciphertext': ciphertext,
                'encrypted_aes_key': encrypted_aes_key,
                'encrypted_hmac_key': encrypted_hmac_key,
                'hmac_signature': hmac_signature,
                'iv': iv,
                'tag': tag
            }
            # --- 添加日志 ---
            logger.debug(f"Encrypt: enc_aes_key hash: {SHA256.new(encrypted_aes_key).hexdigest()}")
            logger.debug(f"Encrypt: enc_hmac_key hash: {SHA256.new(encrypted_hmac_key).hexdigest()}")
            # --- 日志结束 ---
            return result
        except Exception as e:
            raise RuntimeError(f"混合加密失败: {str(e)}")
    #混合解密
    def decrypt(self, ciphertext: bytes, encrypted_aes_key: bytes, 
                encrypted_hmac_key: bytes, hmac_signature: bytes,
                iv: bytes, tag: bytes, key_id: str) -> bytes:
        """
        混合解密
        :param ciphertext: 密文
        :param encrypted_aes_key: 加密的AES密钥
        :param encrypted_hmac_key: 加密的HMAC密钥
        :param hmac_signature: HMAC签名
        :param iv: 初始化向量 (IV)
        :param tag: 认证标签
        :param key_id: 密钥ID
        :return: 明文
        """
        try:
            # 检查key_id是否已经包含'_private'后缀
            base_key_id = key_id.replace('_private', '').replace('_public', '')
            private_key_id = base_key_id + '_private'
            public_key_id = base_key_id + '_public'
            
            # ---- 添加密钥对验证 ----
            try:
                logger.info(f"Verifying key pair for base ID: {base_key_id}")
                priv_key_data, priv_algo = self.key_manager.get_key(private_key_id)
                pub_key_data, pub_algo = self.key_manager.get_key(public_key_id)
                
                if not priv_key_data or priv_algo != 'RSA-PRIVATE':
                    raise ValueError(f"Private key invalid or not found: {private_key_id}")
                if not pub_key_data or pub_algo != 'RSA-PUBLIC':
                     raise ValueError(f"Public key invalid or not found: {public_key_id}")
                     
                priv_key_obj = RSA.import_key(priv_key_data)
                pub_key_obj = RSA.import_key(pub_key_data)
                
                # 检查公钥是否与私钥的公钥部分匹配
                if pub_key_obj != priv_key_obj.publickey():
                     logger.error(f"Key pair mismatch for ID: {base_key_id}")
                     raise ValueError("RSA public and private keys do not match!")
                logger.info("Key pair verified successfully.")
            except Exception as key_err:
                 logger.error(f"Key pair verification failed: {key_err}", exc_info=True)
                 raise RuntimeError(f"RSA密钥对验证失败: {str(key_err)}") from key_err
            # ---- 验证结束 ----
            
            # 使用RSA解密AES密钥 (传递已加载的私钥对象)
            logger.debug(f"Decrypting AES key using verified private key object for ID: {private_key_id}")
            # --- 添加日志 ---
            logger.debug(f"Decrypt Call: enc_aes_key hash: {SHA256.new(encrypted_aes_key).hexdigest()}")
            # --- 日志结束 ---
            aes_key = self.rsa_handler.decrypt(encrypted_aes_key, private_key_obj=priv_key_obj) # 传递对象
            
            # 使用RSA解密HMAC密钥 (传递已加载的私钥对象)
            logger.debug(f"Decrypting HMAC key using verified private key object for ID: {private_key_id}")
            # --- 添加日志 ---
            logger.debug(f"Decrypt Call: enc_hmac_key hash: {SHA256.new(encrypted_hmac_key).hexdigest()}")
            # --- 日志结束 ---
            hmac_key = self.rsa_handler.decrypt(encrypted_hmac_key, private_key_obj=priv_key_obj) # 传递对象
            
            # 验证HMAC
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            hmac.update(ciphertext)
            try:
                hmac.verify(hmac_signature)
            except ValueError:
                raise RuntimeError("HMAC验证失败")
            
            # 使用AES解密明文
            return self.aes_handler.decrypt(ciphertext, aes_key, iv, tag)
        except Exception as e:
            raise RuntimeError(f"混合解密失败: {str(e)}")

    # 文件加密和保存机制
    def encrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """使用混合加密方法加密文件"""
        temp_file = None
        temp_aes_key_id = None
        try:
            logger.info(f"开始混合加密文件: {input_file}")
            
            # 检查输入文件是否存在
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"输入文件不存在: {input_file}")
            
            # 生成AES密钥
            logger.info("生成AES密钥")
            aes_key = get_random_bytes(32)  # 256-bit key
            
            # 为AES密钥生成临时ID并存储
            temp_aes_key_id = f"temp_aes_key_{os.urandom(4).hex()}"
            logger.info(f"存储临时AES密钥: {temp_aes_key_id}")
            self.key_manager.store_key(temp_aes_key_id, aes_key, 'AES-256')
            
            # 使用RSA加密AES密钥
            logger.info("使用RSA加密AES密钥")
            try:
                # 检查key_id是否已经包含'_public'后缀
                rsa_key_id = key_id
                if not key_id.endswith('_public'):
                    rsa_key_id = key_id + '_public'
                logger.info(f"使用RSA公钥ID: {rsa_key_id}")
                
                encrypted_key = self.rsa_handler.encrypt(aes_key, rsa_key_id)
                logger.info("AES密钥加密成功")
            except Exception as e:
                logger.error(f"RSA加密AES密钥失败: {e}")
                raise RuntimeError(f"RSA加密AES密钥失败: {str(e)}")
            
            # 使用AES加密文件
            logger.info("使用AES加密文件")
            temp_file = output_file + '.temp'
            try:
                # 使用密钥ID而不是原始密钥数据
                self.aes_handler.encrypt_file(input_file, temp_file, temp_aes_key_id)
                logger.info("AES文件加密成功")
            except Exception as e:
                logger.error(f"AES加密文件失败: {e}")
                raise RuntimeError(f"AES加密文件失败: {str(e)}")
            finally:
                # 删除临时AES密钥
                try:
                    if temp_aes_key_id:
                        if self.key_manager.delete_key(temp_aes_key_id):
                            logger.info(f"已删除临时AES密钥: {temp_aes_key_id}")
                        else:
                            logger.warning(f"删除临时AES密钥失败: {temp_aes_key_id}")
                except Exception as e:
                    logger.warning(f"删除临时AES密钥失败: {e}")
            
            # 将加密后的AES密钥写入文件头部
            logger.info("写入加密文件")
            try:
                with open(temp_file, 'rb') as f:
                    encrypted_data = f.read()
                
                with open(output_file, 'wb') as f:
                    # 写入加密密钥长度
                    f.write(len(encrypted_key).to_bytes(4, 'big'))
                    # 写入加密后的AES密钥
                    f.write(encrypted_key)
                    # 写入加密后的数据
                    f.write(encrypted_data)
                logger.info("加密文件写入成功")
            except Exception as e:
                logger.error(f"写入加密文件失败: {e}")
                raise RuntimeError(f"写入加密文件失败: {str(e)}")
            
        except Exception as e:
            logger.error(f"混合加密失败: {e}")
            raise RuntimeError(f"混合加密失败: {str(e)}")
        finally:
            # 清理临时文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logger.info(f"已删除临时文件: {temp_file}")
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {e}")
    
    def decrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """使用混合加密方法解密文件"""
        temp_file = None
        temp_aes_key_id = None
        try:
            with open(input_file, 'rb') as f:
                # 读取加密密钥长度
                key_length = int.from_bytes(f.read(4), 'big')
                # 读取加密后的AES密钥
                encrypted_key = f.read(key_length)
                # 读取加密后的数据
                encrypted_data = f.read()
            
            # 检查key_id是否已经包含'_private'后缀
            rsa_key_id = key_id
            if not key_id.endswith('_private'):
                rsa_key_id = key_id + '_private'
            logger.info(f"使用RSA私钥ID: {rsa_key_id}")
            
            # 使用RSA解密AES密钥
            aes_key = self.rsa_handler.decrypt(encrypted_key, rsa_key_id)
            
            # 为AES密钥生成临时ID并存储
            temp_aes_key_id = f"temp_aes_key_{os.urandom(4).hex()}"
            logger.info(f"存储临时AES密钥: {temp_aes_key_id}")
            self.key_manager.store_key(temp_aes_key_id, aes_key, 'AES-256')
            
            # 将加密数据写入临时文件
            temp_file = input_file + '.temp'
            with open(temp_file, 'wb') as f:
                f.write(encrypted_data)
            
            try:
                # 使用AES解密文件
                self.aes_handler.decrypt_file(temp_file, output_file, temp_aes_key_id)
            finally:
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                # 删除临时AES密钥
                try:
                    if temp_aes_key_id:
                        if self.key_manager.delete_key(temp_aes_key_id):
                            logger.info(f"已删除临时AES密钥: {temp_aes_key_id}")
                        else:
                            logger.warning(f"删除临时AES密钥失败: {temp_aes_key_id}")
                except Exception as e:
                    logger.warning(f"删除临时AES密钥失败: {e}")
                    
        except Exception as e:
            raise RuntimeError(f"混合解密失败: {str(e)}")
