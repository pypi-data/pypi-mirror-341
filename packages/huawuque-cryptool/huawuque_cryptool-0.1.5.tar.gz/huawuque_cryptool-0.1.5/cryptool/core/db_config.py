import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('.env')

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'autocommit': True
}

# 验证必要的环境变量
required_env_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME', 'MASTER_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"缺少必要的环境变量: {', '.join(missing_vars)}")

# 主密钥配置
MASTER_KEY = os.getenv('MASTER_KEY')

# 日志配置
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/crypto.log') 