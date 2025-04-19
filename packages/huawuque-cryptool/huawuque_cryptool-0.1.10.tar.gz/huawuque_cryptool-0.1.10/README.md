# 加密工具 (CryptoTool)

这是一个基于Python的加密工具，提供了多种加密算法的实现，包括AES对称加密、RSA非对称加密以及混合加密方案。

## 功能特点

- AES对称加密/解密
- RSA非对称加密/解密
- 混合加密方案（AES + RSA）
- 文件加密/解密支持
- 完整的错误处理和日志记录
- 支持命令行操作

## 系统要求

- Python 3.6 或更高版本
- MySQL 数据库（用于密钥存储）
- 对于 GUI 功能，需要安装 tkinter（Python 标准库的一部分）

## 安装步骤

### 1. 安装系统依赖

#### Windows
```bash
# 安装 MySQL
# 从 https://dev.mysql.com/downloads/installer/ 下载并安装 MySQL

# 安装 Python
# 从 https://www.python.org/downloads/ 下载并安装 Python 3.6+
```

#### Linux (Ubuntu/Debian)
```bash
# 安装 MySQL
sudo apt-get update
sudo apt-get install mysql-server

# 安装 Python 和 tkinter
sudo apt-get install python3 python3-tk python3-pip
```

#### macOS
```bash
# 使用 Homebrew 安装 MySQL
brew install mysql

# 安装 Python（通常已预装）
# 如果需要安装 tkinter
brew install python-tk
```

### 2. 配置 MySQL

```sql
# 登录 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE crypto_keystore;

# 创建用户并授权
CREATE USER 'your_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON crypto_keystore.* TO 'your_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 安装 Python 包

```bash
# 安装加密工具
pip install huawuque-cryptool==0.1.9
```

### 4. 配置环境

1. 创建项目目录：
```bash
mkdir my_crypto_project
cd my_crypto_project
```

2. 创建 `.env` 文件：
```env
# 数据库配置
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=crypto_keystore
DB_PORT=3306

# 主密钥（用于加密存储的敏感信息）
MASTER_KEY=your_master_key

# 日志配置（可选）
LOG_LEVEL=INFO
LOG_FILE=logs/crypto.log
```

3. 初始化数据库：
```bash
# 运行初始化脚本
python -m cryptool.utils.setup_db
```

## 使用方法

### 命令行使用

```bash
# 查看帮助
cryptool --help

# 加密文件
cryptool encrypt --file test.txt --algorithm aes

# 解密文件
cryptool decrypt --file test.txt.enc --algorithm aes

# 生成密钥
cryptool generate-key --algorithm rsa
```

### 图形界面使用

```bash
# 启动图形界面
cryptool-gui
```

## 依赖说明

项目依赖以下 Python 包：

- `python-dotenv>=1.0.0`：用于环境变量管理
- `cryptography>=41.0.0`：用于加密操作
- `python-docx==0.8.11`：用于处理 Word 文档
- `docx2txt==0.8`：用于从 Word 文档提取文本
- `pycryptodome>=3.18.0`：用于加密操作
- `mysql-connector-python>=8.0.0`：用于 MySQL 数据库连接
- `psutil>=5.9.0`：用于系统资源监控

## 注意事项

1. 确保 `.env` 文件中的配置正确
2. 主密钥要妥善保管，不要泄露
3. 加密后的文件要安全存储
4. 定期备份数据库
5. 定期轮换密钥
6. 不要将包含敏感信息的文件提交到版本控制系统 