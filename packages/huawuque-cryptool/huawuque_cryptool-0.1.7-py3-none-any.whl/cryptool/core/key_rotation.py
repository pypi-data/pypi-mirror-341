import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import secrets
import base64
from cryptography.fernet import Fernet

class KeyRotation:
    def __init__(self, rotation_days: int = None):
        """
        初始化密钥轮换管理器
        :param rotation_days: 密钥轮换周期（天），如果为None则从环境变量读取
        """
        # 从环境变量读取轮换周期，如果未设置则使用默认值30天
        if rotation_days is None:
            rotation_days = int(os.getenv('KEY_ROTATION_DAYS', '30'))
        
        self.rotation_days = rotation_days
        self.history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key_history.json")
        self.logger = logging.getLogger(__name__)
        self._load_history()

    def _load_history(self) -> None:
        """加载密钥历史"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception as e:
            self.logger.error(f"加载密钥历史失败: {str(e)}")
            self.history = []

    def _save_history(self) -> None:
        """保存密钥历史"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            self.logger.error(f"保存密钥历史失败: {str(e)}")

    def should_rotate(self) -> bool:
        """
        检查是否需要轮换密钥
        :return: 是否需要轮换
        """
        if not self.history:
            return True
        
        last_key = self.history[-1]
        created_at = datetime.fromisoformat(last_key['created_at'])
        return datetime.now() - created_at > timedelta(days=self.rotation_days)

    def rotate_key(self) -> str:
        """
        生成新的主密钥
        :return: 新的主密钥
        """
        try:
            # 使用Fernet生成正确的密钥格式
            new_key = Fernet.generate_key().decode('utf-8')
            
            # 创建新的密钥记录
            key_info = {
                'key_id': secrets.token_hex(16),
                'created_at': datetime.now().isoformat(),
                'status': 'active',
                'version': len(self.history) + 1
            }
            
            # 添加到历史记录
            self.history.append(key_info)
            self._save_history()
            
            # 更新环境变量
            self._update_env_file(new_key)
            
            self.logger.info("密钥轮换成功")
            return new_key
            
        except Exception as e:
            self.logger.error(f"密钥轮换失败: {str(e)}")
            raise

    def _update_env_file(self, new_key: str) -> None:
        """
        更新环境变量文件中的主密钥
        :param new_key: 新的主密钥
        """
        env_file = ".env"
        try:
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    lines = f.readlines()
                
                # 更新或添加MASTER_KEY
                key_found = False
                for i, line in enumerate(lines):
                    if line.startswith('MASTER_KEY='):
                        lines[i] = f'MASTER_KEY={new_key}\n'
                        key_found = True
                        break
                
                if not key_found:
                    lines.append(f'MASTER_KEY={new_key}\n')
                
                with open(env_file, 'w') as f:
                    f.writelines(lines)
            else:
                with open(env_file, 'w') as f:
                    f.write(f'MASTER_KEY={new_key}\n')
            
            self.logger.info("环境变量文件更新成功")
            
        except Exception as e:
            self.logger.error(f"更新环境变量文件失败: {str(e)}")
            raise

    def get_key_history(self) -> List[Dict[str, Any]]:
        """
        获取密钥历史
        :return: 密钥历史列表
        """
        return self.history