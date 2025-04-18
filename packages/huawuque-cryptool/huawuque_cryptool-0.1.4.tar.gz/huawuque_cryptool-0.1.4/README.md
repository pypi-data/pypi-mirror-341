# 加密工具 (CryptoTool)

这是一个基于Python的加密工具，提供了多种加密算法的实现，包括AES对称加密、RSA非对称加密以及混合加密方案。

## 功能特点

- AES对称加密/解密
- RSA非对称加密/解密
- 混合加密方案（AES + RSA）
- 文件加密/解密支持
- 完整的错误处理和日志记录
- 支持命令行操作

## 安装

### 通过PyPI安装（推荐）

```bash
pip install huawuque-cryptool
```

### 从源码安装

1. 克隆项目到本地：
```bash
git clone https://github.com/huawuque/cryptool.git
cd cryptool
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置

在使用工具之前，您需要配置以下环境变量。创建一个 `.env` 文件在项目根目录，包含以下内容：

```env
# 数据库配置
DB_HOST=localhost
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
DB_PORT=3306

# 主密钥（用于加密存储的敏感信息）
MASTER_KEY=your_master_key

# 日志配置（可选）
LOG_LEVEL=INFO
LOG_FILE=logs/crypto.log
```

注意事项：
1. 所有配置项都是必需的，除了 LOG_LEVEL 和 LOG_FILE
2. 主密钥（MASTER_KEY）应该是足够长的随机字符串
3. 确保数据库已经创建并且用户有适当的权限
4. 不要将包含敏感信息的 .env 文件提交到版本控制系统

## 使用方法

### 命令行使用

安装后，您可以通过`cryptool`命令在命令行中使用该工具：

```bash
# 查看帮助
cryptool --help

# 运行示例演示
cryptool example

# AES加密
cryptool aes-encrypt "要加密的文本"

# AES解密
cryptool aes-decrypt "加密后的文本"

# RSA加密
cryptool rsa-encrypt "要加密的文本"

# RSA解密
cryptool rsa-decrypt "加密后的文本"

# 混合加密（结果保存到文件）
cryptool hybrid-encrypt "要加密的文本"

# 混合解密（从文件读取）
cryptool hybrid-decrypt hybrid_encrypted.json

# Base64编码
cryptool base64-encode "要编码的文本"

# Base64解码
cryptool base64-decode "编码后的文本"
```

### Python代码中使用

```python
from cryptool.core.app import CryptoApp

# 初始化加密工具
app = CryptoApp()

# AES加密示例
text = "这是一个测试文本"
encrypted_aes = app.encrypt_aes(text)
print(f"AES加密后: {encrypted_aes}")
decrypted_aes = app.decrypt_aes(encrypted_aes)
print(f"AES解密后: {decrypted_aes}")

# RSA加密示例
encrypted_rsa = app.encrypt_rsa(text)
print(f"RSA加密后: {encrypted_rsa}")
decrypted_rsa = app.decrypt_rsa(encrypted_rsa)
print(f"RSA解密后: {decrypted_rsa}")

# 混合加密示例
encrypted_hybrid = app.encrypt_hybrid(text)
print(f"混合加密后: {encrypted_hybrid}")
decrypted_hybrid = app.decrypt_hybrid(encrypted_hybrid)
print(f"混合解密后: {decrypted_hybrid}")

# Base64编码示例
encoded = app.encode_base64(text)
print(f"Base64编码后: {encoded}")
decoded = app.decode_base64(encoded)
print(f"Base64解码后: {decoded}")
```

## 注意事项

- 本工具生成的RSA密钥对存储在内存中，每次运行时会生成新的密钥对
- 日志文件默认保存在`logs`目录下
- 混合加密结果通常保存为JSON格式

## 许可证

MIT License 