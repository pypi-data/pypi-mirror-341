import os
import uuid
import logging
from typing import Any, Dict, Optional, List, Union
import importlib
from dotenv import load_dotenv
from cryptool.core.key_management import KeyManager
from cryptool.core.key_rotation import KeyRotation
from cryptool.core.fernet import Fernet
import base64
from hashlib import sha256

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class CryptoCore:
    """加密工具核心类"""
    
    SUPPORTED_MODES = {'encrypt', 'decrypt', 'hash'}
    SUPPORTED_ALGORITHMS = {
        'aes': ('.symmetric', 'AESHandler'),
        'rsa': ('.asymmetric', 'RSAHandler'),
        'hybrid': ('.hybrid', 'HybridHandler'),
        'sha256': ('.hashing', 'SHA256Handler')
    }

    def __init__(self):
        """初始化加密核心"""
        self._init_database()
        self._algorithms: Dict[str, Any] = {}
        logger.info("加密核心初始化完成")

    def _init_database(self):
        """初始化数据库连接"""
        try:
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'user': os.getenv('DB_USER', 'hwq'),
                'password': os.getenv('DB_PASSWORD'),
                'database': os.getenv('DB_NAME', 'crypto_keystore')
            }
            
            # 验证必要的配置
            if not db_config['password']:
                raise ValueError("数据库密码未配置")
            
            self.key_manager = KeyManager(**db_config)
            logger.info("数据库连接初始化成功")
        except Exception as e:
            logger.error(f"数据库初始化失败: {e}")
            raise RuntimeError(f"数据库初始化失败: {str(e)}") from e

    def _load_algorithm(self, algo: str) -> Any:
        """
        按需加载算法模块
        """
        if algo not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(f"不支持的算法: {algo}")

        if algo not in self._algorithms:
            try:
                module_path, class_name = self.SUPPORTED_ALGORITHMS[algo]
                module = importlib.import_module(module_path, package='cryptool.core')
                cls = getattr(module, class_name)
                
                # 根据算法类型传递不同的参数
                if algo == 'aes':
                    self._algorithms[algo] = cls(key_manager=self.key_manager)
                elif algo == 'rsa':
                    self._algorithms[algo] = cls(key_manager=self.key_manager)
                elif algo == 'hybrid':
                    # 确保 AES 和 RSA handlers 已加载
                    aes_handler = self._load_algorithm('aes')
                    rsa_handler = self._load_algorithm('rsa')
                    # 传递所有依赖项给 HybridHandler
                    self._algorithms[algo] = cls(
                        key_manager=self.key_manager, 
                        aes_handler=aes_handler, 
                        rsa_handler=rsa_handler
                    )
                else:
                    self._algorithms[algo] = cls()
                    
                logger.debug(f"成功加载算法: {algo}")
            except Exception as e:
                logger.error(f"加载算法 {algo} 失败: {e}")
                raise RuntimeError(f"加载{algo}算法失败: {str(e)}") from e

        return self._algorithms[algo]

    def execute(self, mode: str, algo: str, data: bytes, key_id: Optional[str] = None, block_size: int = 4096) -> bytes:
        """
        执行加密/解密操作
        
        Args:
            mode: 操作模式，'encrypt'/'decrypt'/'hash'
            algo: 算法类型，'aes'/'rsa'/'hybrid'/'sha256'
            data: 要处理的数据
            key_id: 密钥ID（对称/非对称/混合加密必需）
            block_size: 分块处理的大小，默认4KB
            
        Returns:
            处理后的数据
            
        Raises:
            ValueError: 参数错误
            RuntimeError: 操作失败
        """
        if mode not in self.SUPPORTED_MODES:
            raise ValueError(f"不支持的操作模式: {mode}")

        try:
            handler = self._load_algorithm(algo)
            
            if algo == 'aes':
                if not key_id:
                    raise ValueError("AES加密需要提供密钥ID")
                key = self.key_manager.get_key(key_id)[0]
                if mode == 'encrypt':
                    # 正确接收返回值: ciphertext, iv, tag
                    ciphertext, iv, tag = handler.encrypt(data=data, key=key, block_size=block_size)
                    # 按正确的顺序组合: HYB1 + IV (16 bytes) + Tag (按需，目前为空) + Ciphertext
                    # 假设 tag 即使为空，也预留空间以便将来兼容 GCM 等模式 (例如 16 bytes)
                    # 但当前 AESHandler 返回的 tag 是 b''，所以实际存储为 HYB1 + IV + Ciphertext
                    # 为了简单起见，暂时不预留 tag 空间
                    return b'HYB1' + iv + ciphertext # 存储 HYB1 + IV (16 bytes) + Ciphertext
                else:
                    # 解析加密数据
                    if data[:4] != b'HYB1':
                        raise ValueError("无效的加密数据格式 (HYB1)")
                    # 根据新的存储格式提取: IV 在 HYB1 之后，长度为 16
                    iv = data[4:20]
                    if len(iv) != 16:
                        raise ValueError(f"提取的IV长度不正确: {len(iv)} bytes, 应为 16")
                    # Tag 当前未存储，密文紧随 IV 之后
                    ciphertext = data[20:]
                    # 调用解密，tag 传递空字节
                    return handler.decrypt(encrypted_data=ciphertext, key=key, iv=iv, tag=b'', block_size=block_size)
            elif algo == 'rsa':
                if not key_id:
                    raise ValueError("RSA加密需要提供密钥ID")
                if mode == 'encrypt':
                    # 使用公钥ID进行加密
                    public_key_id = f"{key_id}_public"
                    # RSA 加密处理器不接受 block_size 参数
                    return handler.encrypt(data=data, key_id=public_key_id)
                else:
                    # 使用私钥ID进行解密
                    private_key_id = f"{key_id}_private"
                    # RSA 解密处理器不接受 block_size 参数
                    return handler.decrypt(encrypted_data=data, key_id=private_key_id)
            elif algo == 'hybrid':
                if not key_id:
                    raise ValueError("混合加密需要提供密钥ID")
                if mode == 'encrypt':
                    # 混合加密处理器的 encrypt 方法不接受 block_size 参数
                    result = handler.encrypt(plaintext=data, key_id=key_id)
                    # 结构: HYB1(4) + iv(16) + tag(16) + enc_aes(256) + enc_hmac(256) + sig(32) + cipher
                    # Pad the tag to 16 bytes if it's shorter (e.g., empty from CBC)
                    tag_padded = result['tag'].ljust(16, b'\0')
                    return (
                        b'HYB1' + 
                        result['iv'] + # 使用 iv (16 bytes)
                        tag_padded + # Use padded tag
                        result['encrypted_aes_key'] + 
                        result['encrypted_hmac_key'] + 
                        result['hmac_signature'] + 
                        result['ciphertext']
                    )
                else:
                    params = self._parse_hybrid_params(data)
                    # 混合加密处理器的 decrypt 方法不接受 block_size 参数
                    return handler.decrypt(**params, key_id=key_id)
            elif algo == 'sha256':
                if mode == 'hash':
                    return handler.compute_hash(data)
                else:
                    raise ValueError(f"不支持的哈希操作模式: {mode}")
            else:
                raise ValueError(f"不支持的算法类型: {algo}")
                
        except AttributeError:
            raise NotImplementedError(f"算法 {algo} 不支持 {mode} 操作")
        except Exception as e:
            logger.error(f"{algo} {mode} 操作失败: {e}")
            raise RuntimeError(f"{algo} {mode} 操作失败: {str(e)}") from e

    def generate_key(self, algo_type: str, key_id: Optional[str] = None) -> str:
        """
        生成新密钥
        """
        try:
            if not key_id:
                key_id = str(uuid.uuid4())
                
            if algo_type == 'aes':
                return self.key_manager.generate_key('AES-256', key_id=key_id)
            elif algo_type == 'rsa':
                # 调用 generate_key 并指定算法为 RSA
                return self.key_manager.generate_key('RSA', key_id=key_id)
            elif algo_type == 'hybrid':
                # 混合加密也调用 generate_key 并指定算法为 hybrid
                # KeyManager.generate_key 内部会处理 RSA 密钥对的生成
                return self.key_manager.generate_key('hybrid', key_id=key_id)
            else:
                raise ValueError(f"不支持的算法类型: {algo_type}")
        except Exception as e:
            logger.error(f"生成密钥失败: {e}", exc_info=True)
            raise RuntimeError(f"生成密钥失败: {str(e)}") from e

    def _parse_hybrid_params(self, data: bytes) -> dict:
        """
        解析混合加密的参数
        结构: HYB1(4) + iv(16) + tag(16) + enc_aes(256) + enc_hmac(256) + sig(32) + cipher
        """
        try:
            # 检查最小长度
            min_len = 4 + 16 + 16 + 256 + 256 + 32
            if len(data) < min_len:
                raise ValueError(f"混合加密数据过短: {len(data)} bytes, 至少需要 {min_len}")
                
            # 前4字节是标识符
            if data[:4] != b'HYB1':
                raise ValueError("无效的混合加密数据格式 (HYB1)")
                
            # 解析各个部分
            offset = 4
            iv = data[offset:offset+16]; offset += 16   # 解析 iv (16 bytes)
            tag = data[offset:offset+16]; offset += 16   # 解析 tag (16 bytes)
            encrypted_aes_key = data[offset:offset+256]; offset += 256
            encrypted_hmac_key = data[offset:offset+256]; offset += 256
            hmac_signature = data[offset:offset+32]; offset += 32
            ciphertext = data[offset:]
            
            parsed_result = {
                'ciphertext': ciphertext,
                'encrypted_aes_key': encrypted_aes_key,
                'encrypted_hmac_key': encrypted_hmac_key,
                'hmac_signature': hmac_signature,
                'iv': iv,   # 返回 'iv'
                'tag': tag
            }
            # --- 添加日志 --- # (日志仍然有用)
            logger.debug(f"Parse: enc_aes_key hash: {sha256(encrypted_aes_key).hexdigest()}")
            logger.debug(f"Parse: enc_hmac_key hash: {sha256(encrypted_hmac_key).hexdigest()}")
            # --- 日志结束 --- #
            return parsed_result
        except Exception as e:
            logger.error(f"解析混合加密参数失败: {e}", exc_info=True)
            raise ValueError(f"解析混合加密参数失败: {str(e)}")

    def revoke_key(self, key_id: str) -> None:
        """
        吊销密钥
        
        Args:
            key_id: 要吊销的密钥ID
            
        Raises:
            ValueError: 无效的密钥ID
            RuntimeError: 吊销失败
        """
        try:
            if not key_id:
                raise ValueError("密钥ID不能为空")
            self.key_manager.revoke_key(key_id)
            logger.info(f"成功吊销密钥: {key_id}")
        except Exception as e:
            logger.error(f"吊销密钥失败: {e}")
            
    def encode_base64(self, data: Union[str, bytes]) -> bytes:
        """
        Base64编码
        
        Args:
            data: 要编码的数据，可以是字符串或字节
            
        Returns:
            编码后的字节数据
            
        Raises:
            RuntimeError: 编码失败
        """
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            return base64.b64encode(data)
        except Exception as e:
            logger.error(f"Base64编码失败: {e}")
            raise RuntimeError(f"Base64编码失败: {str(e)}") from e
            
    def decode_base64(self, data: Union[str, bytes]) -> bytes:
        """
        Base64解码
        
        Args:
            data: 要解码的Base64数据，可以是字符串或字节
            
        Returns:
            解码后的字节数据
            
        Raises:
            RuntimeError: 解码失败
        """
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            return base64.b64decode(data)
        except Exception as e:
            logger.error(f"Base64解码失败: {e}")
            raise RuntimeError(f"Base64解码失败: {str(e)}") from e
            
    def cleanup(self) -> None:
        """清理资源"""
        try:
            if hasattr(self, 'key_manager'):
                self.key_manager.close()
                logger.info("成功清理资源")
        except Exception as e:
            logger.error(f"清理资源失败: {e}")

    def __del__(self):
        """析构函数"""
        self.cleanup()

class App:
    def __init__(self):
        self.key_rotation = KeyRotation()
        self.fernet = self._load_master_key()
        self.logger = logging.getLogger(__name__)

    def _load_master_key(self):
        """加载主密钥，如果需要则进行轮换"""
        try:
            master_key = os.getenv('MASTER_KEY')
            if not master_key:
                raise ValueError("未配置MASTER_KEY环境变量")
            
            # 检查是否需要轮换密钥
            if self.key_rotation.should_rotate():
                self.logger.info("检测到需要轮换密钥")
                master_key = self.key_rotation.rotate_key()
            
            return Fernet(master_key.encode())
        except Exception as e:
            self.logger.error(f"加载主密钥失败: {str(e)}")
            raise

    def encrypt_file(self, file_path: str) -> str:
        """加密单个文件"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted_data = self.fernet.encrypt(data)
            output_path = f"{file_path}.enc"
            
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)
            
            self.logger.info(f"文件加密成功: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"文件加密失败: {str(e)}")
            raise

    def decrypt_file(self, file_path: str) -> str:
        """解密单个文件"""
        try:
            if not file_path.endswith('.enc'):
                raise ValueError("文件必须是加密文件(.enc后缀)")
            
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            output_path = file_path[:-4]  # 移除.enc后缀
            
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            self.logger.info(f"文件解密成功: {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"文件解密失败: {str(e)}")
            raise

    def batch_encrypt_files(self, file_paths: List[str]) -> Dict[str, str]:
        """批量加密文件"""
        results = {}
        for file_path in file_paths:
            try:
                output_path = self.encrypt_file(file_path)
                results[file_path] = output_path
            except Exception as e:
                results[file_path] = f"加密失败: {str(e)}"
        return results

    def batch_decrypt_files(self, file_paths: List[str]) -> Dict[str, str]:
        """批量解密文件"""
        results = {}
        for file_path in file_paths:
            try:
                output_path = self.decrypt_file(file_path)
                results[file_path] = output_path
            except Exception as e:
                results[file_path] = f"解密失败: {str(e)}"
        return results

    def encode_base64(self, data: Union[str, bytes]) -> str:
        """Base64编码"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            return base64.b64encode(data).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Base64编码失败: {str(e)}")
            raise

    def decode_base64(self, data: str) -> Union[str, bytes]:
        """Base64解码"""
        try:
            decoded = base64.b64decode(data)
            try:
                return decoded.decode('utf-8')
            except UnicodeDecodeError:
                return decoded
        except Exception as e:
            self.logger.error(f"Base64解码失败: {str(e)}")
            raise

    def get_key_history(self) -> List[Dict[str, Any]]:
        """获取密钥历史"""
        return self.key_rotation.get_key_history()

    def manual_key_rotation(self) -> bool:
        """手动触发密钥轮换"""
        try:
            self.key_rotation.rotate_key()
            self.fernet = self._load_master_key()
            return True
        except Exception as e:
            self.logger.error(f"手动密钥轮换失败: {str(e)}")
            return False