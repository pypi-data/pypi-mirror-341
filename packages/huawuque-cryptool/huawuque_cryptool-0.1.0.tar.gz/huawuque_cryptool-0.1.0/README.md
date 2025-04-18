# 加密工具 (CryptoTool)

这是一个基于Python的加密工具，提供了多种加密算法的实现，包括AES对称加密、RSA非对称加密以及混合加密方案。

## 功能特点

- AES对称加密/解密
- RSA非对称加密/解密
- 混合加密方案（AES + RSA）
- 文件加密/解密支持
- 完整的错误处理和日志记录

## 安装

1. 克隆项目到本地：
```bash
git clone https://github.com/yourusername/EncryptionTool.git
cd EncryptionTool
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

## 使用方法

### 基本使用

```python
from cryptool.core.app import CryptoApp

# 初始化加密工具
app = CryptoApp()

# 生成密钥
aes_key = app.generate_aes_key()
rsa_public_key, rsa_private_key = app.generate_rsa_keys()

# 加密/解密示例
text = "Hello, World!"
encrypted_text = app.encrypt(text, aes_key)
decrypted_text = app.decrypt(encrypted_text, aes_key)
```

### 文件加密

```python
from cryptool.core.symmetric import AESHandler

# 加密文件
AESHandler.encrypt_file("input.txt", "encrypted.txt", aes_key)

# 解密文件
AESHandler.decrypt_file("encrypted.txt", "decrypted.txt", aes_key)
```

### 混合加密

```python
from cryptool.core.hybrid import HybridHandler

# 生成混合加密参数
hybrid_params = app.generate_hybrid_params()

# 加密
encrypted_text = HybridHandler.encrypt(text, hybrid_params)

# 解密
decrypted_text = HybridHandler.decrypt(encrypted_text, hybrid_params)
```

## 配置

项目使用`.env`文件进行配置，主要配置项包括：

- `AES_KEY_LENGTH`: AES密钥长度（默认32字节）
- `RSA_KEY_SIZE`: RSA密钥大小（默认2048位）
- `LOG_LEVEL`: 日志级别（默认INFO）

## 示例

查看`example.py`文件获取更多使用示例。

## 许可证

MIT License 