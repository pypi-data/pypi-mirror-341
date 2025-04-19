import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from cryptool.gui.main_window import CryptoGUI

# 配置日志
def setup_logging():
    """配置日志系统"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "cryptool.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_environment():
    """检查运行环境"""
    logger = logging.getLogger(__name__)
    
    # 检查环境变量
    if not load_dotenv():
        logger.error("无法加载环境变量文件")
        return False
        
    required_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"缺少必要的环境变量: {', '.join(missing_vars)}")
        return False
        
    return True

def main():
    """主程序入口"""
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # 检查环境
        if not check_environment():
            sys.exit(1)
            
        # 启动GUI
        logger.info("启动加密工具")
        app = CryptoGUI()
        app.mainloop()
        
    except Exception as e:
        logger.error(f"程序运行时错误: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("程序退出")

if __name__ == '__main__':
    main() 