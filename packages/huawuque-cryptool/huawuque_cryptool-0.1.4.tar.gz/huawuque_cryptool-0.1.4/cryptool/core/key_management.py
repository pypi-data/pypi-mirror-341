import mysql.connector
from .db_config import DB_CONFIG
from datetime import datetime
import os
from Crypto.PublicKey import RSA
from typing import Tuple, Union, Optional
import time
import logging
from .fernet import Fernet

logger = logging.getLogger(__name__)

class KeyManager:
    def __init__(self, **db_config):
        self.max_retries = 3
        self.retry_delay = 1
        self.conn = None
        self.cursor = None
        self.db_config = db_config or DB_CONFIG
        self.fernet = self._init_fernet()  # 初始化Fernet
        self.logger = logging.getLogger(__name__)  # 添加logger
        self._init_db()
        
    def _init_fernet(self):
        """初始化Fernet加密器"""
        try:
            master_key = os.getenv('MASTER_KEY')
            if not master_key:
                raise ValueError("未配置MASTER_KEY环境变量")
            elif not self._is_valid_fernet_key(master_key):
                raise ValueError("MASTER_KEY格式不正确，请确保是32字节的url-safe base64编码")
            
            return Fernet(master_key.encode())
        except Exception as e:
            logger.error(f"初始化Fernet失败: {str(e)}")
            raise
        
    def _is_valid_fernet_key(self, key: str) -> bool:
        """验证Fernet密钥格式"""
        try:
            # Fernet密钥必须是32字节的url-safe base64编码
            if len(key) != 44:  # 32字节base64编码后的长度
                return False
            # 尝试解码验证
            Fernet(key.encode())
            return True
        except:
            return False
        
    def _init_db(self):
        """初始化数据库连接"""
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                self.conn = mysql.connector.connect(**self.db_config)
                self.cursor = self.conn.cursor()
                self._create_tables()
                logger.info("数据库表初始化成功")
                break
            except Exception as e:
                retry_count += 1
                if retry_count >= self.max_retries:
                    logger.error(f"数据库初始化失败，已达到最大重试次数: {str(e)}")
                    raise
                logger.error(f"数据库初始化失败，正在重试 ({retry_count}/{self.max_retries}): {str(e)}")
                time.sleep(self.retry_delay)
                if self.conn:
                    self.conn.close()
                if self.cursor:
                    self.cursor.close()
                    
    def _create_tables(self):
        """创建数据库表"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS `encryption_keys` (
                id VARCHAR(64) PRIMARY KEY,
                wrapped_key BLOB NOT NULL,
                algorithm VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NULL,
                version INT NOT NULL DEFAULT 1,
                status VARCHAR(10) DEFAULT 'active'
            )
        """)
        self.conn.commit()
        
    def store_key(self, key_id: str, key_data: bytes, algorithm: str) -> None:
        """存储密钥"""
        # 添加存储前的格式验证
        if algorithm == 'RSA':
            if not key_data.startswith(b'-----BEGIN'):
                raise ValueError("密钥必须为PEM格式")
            if b'PUBLIC KEY' in key_data and not self.verify_rsa_key(key_data):
                raise ValueError("无效的RSA公钥格式")
        
        # 使用Fernet加密密钥数据
        try:
            encrypted_key_data = self.fernet.encrypt(key_data)
            
            self.cursor.execute("""
                INSERT INTO encryption_keys 
                (id, wrapped_key, algorithm, created_at, status, version)
                VALUES (%s, %s, %s, NOW(), 'active', 1)
                ON DUPLICATE KEY UPDATE
                wrapped_key = VALUES(wrapped_key),
                algorithm = VALUES(algorithm),
                version = version + 1,
                status = 'active'
            """, (key_id, encrypted_key_data, algorithm))
            self.conn.commit()
        except mysql.connector.Error as err:
            self.conn.rollback()
            logger.error(f"密钥存储失败: {err}")
            raise
            
    def get_key(self, key_id: str) -> Tuple[bytes, str]:
        """获取密钥"""
        try:
            self.cursor.execute(
                """
                SELECT wrapped_key, algorithm FROM encryption_keys 
                WHERE id = %s AND status = 'active'
                """,
                (key_id,)
            )
            result = self.cursor.fetchone()
            if not result:
                return None, None
                
            # 使用Fernet解密密钥数据
            encrypted_key_data, algorithm = result
            key_data = self.fernet.decrypt(encrypted_key_data)
            
            return key_data, algorithm
        except Exception as e:
            raise RuntimeError(f"获取密钥失败: {str(e)}")
            
    def generate_key(self, algorithm: str, key_id: str) -> str:
        """生成密钥并返回其ID"""
        try:
            if algorithm == 'AES-256':
                key = os.urandom(32)
                self.store_key(key_id, key, algorithm)
                return key_id # 返回key_id
            elif algorithm == 'RSA' or algorithm == 'hybrid': # Combined logic for RSA key pair generation
                logger.info(f"Generating RSA key pair ({algorithm}) with ID base: {key_id}")
                key = RSA.generate(2048)
                # Export private key in PKCS#8 PEM format
                private_key_pem = key.export_key(format='PEM', pkcs=8, protection=None) # Ensure no password protection
                # Export public key in SubjectPublicKeyInfo PEM format
                public_key_pem = key.publickey().export_key(format='PEM')
                
                # Store private key
                private_key_id = key_id + '_private'
                self.store_key(private_key_id, private_key_pem, 'RSA-PRIVATE')
                logger.debug(f"Stored private key {private_key_id}")
                
                # Store public key
                public_key_id = key_id + '_public'
                self.store_key(public_key_id, public_key_pem, 'RSA-PUBLIC')
                logger.debug(f"Stored public key {public_key_id}")
                
                return key_id # Return the base key_id
            else:
                raise ValueError(f"不支持的算法类型: {algorithm}")
        except Exception as e:
            raise RuntimeError(f"生成密钥失败: {str(e)}")
            
    def verify_rsa_key(self, key_data: bytes) -> bool:
        """验证RSA密钥格式"""
        try:
            if not isinstance(key_data, bytes):
                logger.error("密钥数据不是字节类型")
                return False
                
            if not key_data.startswith(b'-----BEGIN'):
                logger.error("密钥不是PEM格式")
                return False
                
            try:
                key = RSA.import_key(key_data)
                if b'PUBLIC KEY' in key_data:
                    # 验证公钥
                    if not key.has_private():
                        return True
                    logger.error("公钥包含私钥信息")
                    return False
                elif b'PRIVATE KEY' in key_data:
                    # 验证私钥
                    if key.has_private():
                        return True
                    logger.error("私钥格式不正确")
                    return False
                else:
                    logger.error("未知的密钥类型")
                    return False
            except Exception as e:
                logger.error(f"密钥解析失败: {str(e)}")
                return False
        except Exception as e:
            logger.error(f"密钥验证失败: {str(e)}")
            return False
            
    def delete_key(self, key_id: str) -> bool:
        """删除密钥"""
        try:
            self.cursor.execute(
                """
                DELETE FROM encryption_keys WHERE id = %s
                """,
                (key_id,)
            )
            self.conn.commit()
            affected_rows = self.cursor.rowcount
            return affected_rows > 0
        except Exception as e:
            logger.error(f"删除密钥失败: {str(e)}")
            return False
            
    def revoke_key(self, key_id: str) -> None:
        """吊销密钥 (更新状态为 'revoked')"""
        try:
            self.cursor.execute(
                """
                UPDATE encryption_keys SET status = 'revoked' 
                WHERE id = %s
                """,
                (key_id,)
            )
            self.conn.commit()
            if self.cursor.rowcount == 0:
                logger.warning(f"尝试吊销不存在或已吊销的密钥: {key_id}")
                # 根据需求，可以选择抛出错误或仅记录警告
                # raise ValueError(f"未找到要吊销的密钥: {key_id}") 
            else:
                logger.info(f"成功吊销密钥: {key_id}")
        except mysql.connector.Error as err:
            self.conn.rollback()
            logger.error(f"吊销密钥失败: {err}")
            raise RuntimeError(f"数据库操作失败: {str(err)}") from err
        except Exception as e:
            logger.error(f"吊销密钥时发生意外错误: {e}")
            raise RuntimeError(f"吊销密钥失败: {str(e)}") from e
            
    def delete_all_keys(self) -> None:
        """删除表中的所有密钥 (使用 TRUNCATE)"""
        try:
            self.logger.warning("准备删除 encryption_keys 表中的所有密钥！")
            # 使用 TRUNCATE TABLE 通常比 DELETE FROM 更快，并且会重置自增ID（如果适用）
            self.cursor.execute("TRUNCATE TABLE encryption_keys;")
            self.conn.commit() # TRUNCATE 在某些数据库中可能是隐式提交，但显式提交更安全
            self.logger.info("已成功删除 encryption_keys 表中的所有密钥。")
        except mysql.connector.Error as err:
            self.conn.rollback()
            logger.error(f"删除所有密钥失败: {err}")
            raise RuntimeError(f"数据库操作失败: {str(err)}") from err
        except Exception as e:
            logger.error(f"删除所有密钥时发生意外错误: {e}")
            raise RuntimeError(f"删除所有密钥失败: {str(e)}") from e
            
    def __del__(self):
        """清理资源"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                try:
                    self.cursor.close()
                except:
                    pass
                    
            if hasattr(self, 'conn') and self.conn:
                try:
                    self.conn.close()
                except:
                    pass
        except:
            # 忽略销毁对象时的任何异常
            pass

    def close(self):
        """关闭数据库连接"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
            self.logger.info("数据库连接已关闭")
