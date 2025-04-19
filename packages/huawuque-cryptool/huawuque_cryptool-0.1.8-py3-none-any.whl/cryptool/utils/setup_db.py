import os
import mysql.connector
from dotenv import load_dotenv
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_database():
    """初始化数据库和表"""
    try:
        # 加载环境变量
        load_dotenv('.env')
        
        # 获取数据库配置
        db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_NAME'),
            'port': int(os.getenv('DB_PORT', '3306')),
        }
        
        # 连接数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # 创建密钥表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS `keys` (
                id VARCHAR(36) PRIMARY KEY,
                algorithm VARCHAR(50) NOT NULL,
                key_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NULL,
                is_revoked BOOLEAN DEFAULT FALSE,
                revoked_at TIMESTAMP NULL
            )
        """)
        
        # 创建加密记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS encryption_records (
                id VARCHAR(36) PRIMARY KEY,
                file_path VARCHAR(255) NOT NULL,
                algorithm VARCHAR(50) NOT NULL,
                key_id VARCHAR(36),
                encrypted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (key_id) REFERENCES `keys`(id)
            )
        """)
        
        # 提交更改
        conn.commit()
        logger.info("数据库初始化成功")
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database()