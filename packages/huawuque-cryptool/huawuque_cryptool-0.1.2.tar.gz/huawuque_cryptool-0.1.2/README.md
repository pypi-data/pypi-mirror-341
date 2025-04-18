# 加密工具 (CryptoTool)

这是一个基于Python的加密工具，提供了多种加密算法的实现，包括AES对称加密、RSA非对称加密、混合加密方案、哈希计算和Base64编码/解码。支持图形用户界面 (GUI) 和命令行接口 (CLI)，并能处理大文件（通过分块加密）。

## 功能特点

- AES、RSA、混合 加密/解密 (支持文件和文本)
- SHA256 哈希计算
- Base64 编码/解码
- 密钥管理 (生成、吊销、列表 - 列表功能待实现)
- 图形用户界面 (GUI)
- 命令行接口 (CLI)
- 支持大文件分块处理 (由核心逻辑实现，具体看实现细节)

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
# 如果需要，也可以直接安装本包
# pip install .
```

## 使用方法

### 图形用户界面 (GUI)

安装后，如果您想使用图形界面，可以运行：

```bash
# (需要系统已正确配置Python环境)
cryptool-gui 
```

(注意：如果上述命令无效，可能需要检查您的Python环境路径配置，或者直接运行Python脚本 `python -m cryptool.gui.main_window`)

### 命令行接口 (CLI)

安装后，您可以通过`cryptool`命令在命令行中使用该工具。

**基本用法:** `cryptool <command> [options]`

**命令列表:**

*   `key`: 密钥管理
    *   `generate -t <aes|rsa>`: 生成指定类型的密钥。
    *   `revoke -t <aes|rsa> -i <key_id>`: 吊销指定ID的密钥。
    *   `list -t <aes|rsa>`: 列出指定类型的密钥 (待实现)。
*   `encrypt`: 加密文件
    *   `-a <aes|rsa|hybrid>`: 指定加密算法。
    *   `-i <input_file>`: 指定输入文件路径。
    *   `-o <output_file>`: 指定输出文件路径。
    *   `-k <key_id>`: 指定使用的密钥ID (混合加密必需)。
*   `decrypt`: 解密文件
    *   `-a <aes|rsa|hybrid>`: 指定解密算法。
    *   `-i <input_file>`: 指定输入文件路径。
    *   `-o <output_file>`: 指定输出文件路径。
    *   `-k <key_id>`: 指定使用的密钥ID (混合解密必需)。
*   `hash`: 计算文件哈希
    *   `-a <sha256>`: 指定哈希算法。
    *   `-i <input_file>`: 指定输入文件路径。
*   `base64`: Base64 编码/解码
    *   `encode -i <input_file> -o <output_file>`: 对文件进行Base64编码。
    *   `decode -i <input_file> -o <output_file>`: 对文件进行Base64解码。

**示例:**

```bash
# 生成AES密钥
cryptool key generate -t aes

# 使用AES加密文件 (假设生成的密钥ID是 aes_key_123)
cryptool encrypt -a aes -i plain.txt -o encrypted.enc -k aes_key_123

# 使用AES解密文件
cryptool decrypt -a aes -i encrypted.enc -o decrypted.txt -k aes_key_123

# 计算文件SHA256哈希
cryptool hash -a sha256 -i important_doc.pdf

# Base64编码文件
cryptool base64 encode -i image.png -o image_base64.txt
```

### Python代码中使用

(这部分可以保留或根据您的核心类 `CryptoCore` 的实际用法进行调整)

```python
from cryptool.core.app import CryptoCore

# 初始化核心
core = CryptoCore()

# 生成AES密钥
key_id = core.generate_key('aes')
print(f"Generated AES key ID: {key_id}")

# 读取文件数据
with open('my_file.txt', 'rb') as f:
    data_to_encrypt = f.read()

# 加密数据
encrypted_data = core.execute(
    mode='encrypt', 
    algo='aes', 
    data=data_to_encrypt, 
    key_id=key_id
)

# 保存加密数据
with open('my_file.enc', 'wb') as f:
    f.write(encrypted_data)

# 解密数据
decrypted_data = core.execute(
    mode='decrypt', 
    algo='aes', 
    data=encrypted_data, 
    key_id=key_id
)

# 保存解密数据
with open('my_file_decrypted.txt', 'wb') as f:
    f.write(decrypted_data)

print("File encryption and decryption example complete.")

# (确保在使用完后关闭 KeyManager)
core.key_manager.close()
```

## 配置

项目可能使用`.env`文件进行配置，或者有其他的配置机制（请根据实际情况说明）。

## 注意事项

- 密钥默认存储在项目根目录下的`keys`目录（或数据库，请根据`KeyManager`实现说明）。
- 日志文件默认保存在`logs`目录下。

## 许可证

MIT License 