# 安全存储工具
"""
提供安全的数据存储功能，包括：
- 敏感数据的加密存储
- 配置信息的安全管理
- 临时数据的清理
"""

import os
import json
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class SecureStorage:
    def __init__(self):
        load_dotenv()
        self._key = self._get_or_generate_key()
        self._fernet = Fernet(self._key)
        
    def _get_or_generate_key(self) -> bytes:
        """获取或生成加密密钥"""
        key = os.getenv('STORAGE_KEY')
        if key:
            return key.encode()
        else:
            key = Fernet.generate_key()
            # 将新生成的密钥保存到环境变量
            with open('.env', 'a') as f:
                f.write(f"\nSTORAGE_KEY={key.decode()}\n")
            return key
            
    def encrypt_data(self, data: Any) -> bytes:
        """加密数据"""
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
        return self._fernet.encrypt(str(data).encode())
        
    def decrypt_data(self, encrypted_data: bytes) -> Any:
        """解密数据"""
        decrypted = self._fernet.decrypt(encrypted_data).decode()
        try:
            return json.loads(decrypted)
        except json.JSONDecodeError:
            return decrypted
            
    def save_secure_config(self, config: Dict[str, Any], filepath: str):
        """安全保存配置信息"""
        encrypted = self.encrypt_data(config)
        with open(filepath, 'wb') as f:
            f.write(encrypted)
            
    def load_secure_config(self, filepath: str) -> Optional[Dict[str, Any]]:
        """安全加载配置信息"""
        try:
            with open(filepath, 'rb') as f:
                encrypted = f.read()
            return self.decrypt_data(encrypted)
        except FileNotFoundError:
            return None
            
    def clear_temp_data(self, directory: str):
        """清理临时数据"""
        for filename in os.listdir(directory):
            if filename.endswith('.tmp'):
                try:
                    os.remove(os.path.join(directory, filename))
                except Exception as e:
                    print(f"清理临时文件失败: {str(e)}")
                    
    def secure_delete(self, filepath: str, passes: int = 3):
        """安全删除文件（多次覆写）"""
        if not os.path.exists(filepath):
            return
            
        file_size = os.path.getsize(filepath)
        with open(filepath, 'wb') as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
                
        os.remove(filepath)
