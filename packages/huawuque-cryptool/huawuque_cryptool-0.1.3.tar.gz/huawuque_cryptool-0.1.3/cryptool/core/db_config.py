import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('venv/.env')

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'hwq'),
    'password': os.getenv('DB_PASSWORD', 'xPWQ3Yra.'),
    'database': os.getenv('DB_NAME', 'crypto_keystore'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'autocommit': True
}

# 主密钥配置
MASTER_KEY = os.getenv('MASTER_KEY', '7X3lPyY5HFkO9JqGvNmWx4jR2bTcAhS8')

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/crypto.log') 