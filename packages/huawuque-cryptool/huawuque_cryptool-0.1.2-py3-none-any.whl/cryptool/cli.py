#!/usr/bin/env python
"""
加密工具命令行接口
支持AES、RSA和混合加密/解密操作，以及文件加密/解密
"""
import os
import sys
import argparse
import json
from cryptool.core.app import CryptoApp

def main():
    """命令行主入口"""
    parser = argparse.ArgumentParser(description="加密工具 - 多种加密算法支持")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # AES加密子命令
    aes_encrypt_parser = subparsers.add_parser("aes-encrypt", help="AES加密")
    aes_encrypt_parser.add_argument("text", help="要加密的文本")
    
    # AES解密子命令
    aes_decrypt_parser = subparsers.add_parser("aes-decrypt", help="AES解密")
    aes_decrypt_parser.add_argument("text", help="要解密的文本")
    
    # RSA加密子命令
    rsa_encrypt_parser = subparsers.add_parser("rsa-encrypt", help="RSA加密")
    rsa_encrypt_parser.add_argument("text", help="要加密的文本")
    
    # RSA解密子命令
    rsa_decrypt_parser = subparsers.add_parser("rsa-decrypt", help="RSA解密")
    rsa_decrypt_parser.add_argument("text", help="要解密的文本")
    
    # 混合加密子命令
    hybrid_encrypt_parser = subparsers.add_parser("hybrid-encrypt", help="混合加密")
    hybrid_encrypt_parser.add_argument("text", help="要加密的文本")
    
    # 混合解密子命令
    hybrid_decrypt_parser = subparsers.add_parser("hybrid-decrypt", help="混合解密")
    hybrid_decrypt_parser.add_argument("file", help="包含加密数据的JSON文件")
    
    # Base64编码子命令
    base64_encode_parser = subparsers.add_parser("base64-encode", help="Base64编码")
    base64_encode_parser.add_argument("text", help="要编码的文本")
    
    # Base64解码子命令
    base64_decode_parser = subparsers.add_parser("base64-decode", help="Base64解码")
    base64_decode_parser.add_argument("text", help="要解码的文本")
    
    # 示例命令
    subparsers.add_parser("example", help="运行示例演示")
    
    args = parser.parse_args()
    
    # 初始化加密工具
    app = CryptoApp()
    
    # 处理命令
    if args.command == "aes-encrypt":
        result = app.encrypt_aes(args.text)
        print(f"加密结果: {result}")
    
    elif args.command == "aes-decrypt":
        result = app.decrypt_aes(args.text)
        print(f"解密结果: {result}")
    
    elif args.command == "rsa-encrypt":
        result = app.encrypt_rsa(args.text)
        print(f"加密结果: {result}")
    
    elif args.command == "rsa-decrypt":
        result = app.decrypt_rsa(args.text)
        print(f"解密结果: {result}")
    
    elif args.command == "hybrid-encrypt":
        result = app.encrypt_hybrid(args.text)
        # 保存到文件
        filename = "hybrid_encrypted.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"混合加密结果已保存到文件: {filename}")
    
    elif args.command == "hybrid-decrypt":
        try:
            with open(args.file, 'r') as f:
                encrypted_data = json.load(f)
            result = app.decrypt_hybrid(encrypted_data)
            print(f"解密结果: {result}")
        except Exception as e:
            print(f"解密失败: {str(e)}")
    
    elif args.command == "base64-encode":
        result = app.encode_base64(args.text)
        print(f"编码结果: {result}")
    
    elif args.command == "base64-decode":
        result = app.decode_base64(args.text)
        print(f"解码结果: {result}")
    
    elif args.command == "example":
        run_example(app)
    
    else:
        parser.print_help()

def run_example(app):
    """运行示例演示"""
    # 示例文本
    text = "这是一个测试文本"
    
    # AES加密示例
    print("\n=== AES加密示例 ===")
    encrypted_aes = app.encrypt_aes(text)
    print(f"加密后: {encrypted_aes}")
    decrypted_aes = app.decrypt_aes(encrypted_aes)
    print(f"解密后: {decrypted_aes}")
    
    # RSA加密示例
    print("\n=== RSA加密示例 ===")
    encrypted_rsa = app.encrypt_rsa(text)
    print(f"加密后: {encrypted_rsa}")
    decrypted_rsa = app.decrypt_rsa(encrypted_rsa)
    print(f"解密后: {decrypted_rsa}")
    
    # 混合加密示例
    print("\n=== 混合加密示例 ===")
    encrypted_hybrid = app.encrypt_hybrid(text)
    print(f"加密后: {encrypted_hybrid}")
    decrypted_hybrid = app.decrypt_hybrid(encrypted_hybrid)
    print(f"解密后: {decrypted_hybrid}")
    
    # Base64编码示例
    print("\n=== Base64编码示例 ===")
    encoded = app.encode_base64(text)
    print(f"编码后: {encoded}")
    decoded = app.decode_base64(encoded)
    print(f"解码后: {decoded}")

if __name__ == "__main__":
    main() 