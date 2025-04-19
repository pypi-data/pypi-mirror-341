# 命令行接口
import argparse
import sys
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from cryptool.core.app import CryptoCore
from cryptool.core.key_management import KeyManager

class CryptoCli:
    def __init__(self):
        try:
            self.core = CryptoCore()
            self.parser = self._build_parser()
        except Exception as e:
            print(f"初始化失败: {str(e)}", file=sys.stderr)
            sys.exit(1)
        
    def _build_parser(self):
        parser = argparse.ArgumentParser(prog='cryptool', description="加密工具命令行版")
        subparsers = parser.add_subparsers(dest='command', required=True)

        # 加密命令
        enc_parser = subparsers.add_parser('encrypt', help='加密操作')
        enc_parser.add_argument('-a', '--algo', 
            choices=['aes', 'rsa', 'hybrid'], required=True)
        enc_parser.add_argument('-i', '--input', required=True, help='输入文件路径')
        enc_parser.add_argument('-o', '--output', required=True, help='输出文件路径')
        enc_parser.add_argument('-k', '--key-id', help='密钥ID（混合加密必需）')

        # 解密命令
        dec_parser = subparsers.add_parser('decrypt', help='解密操作')
        dec_parser.add_argument('-a', '--algo', 
            choices=['aes', 'rsa', 'hybrid'], required=True)
        dec_parser.add_argument('-i', '--input', required=True, help='输入文件路径')
        dec_parser.add_argument('-o', '--output', required=True, help='输出文件路径')
        dec_parser.add_argument('-k', '--key-id', help='密钥ID（混合加密必需）')

        # 哈希命令
        hash_parser = subparsers.add_parser('hash', help='哈希计算')
        hash_parser.add_argument('-a', '--algo', choices=['sha256'], required=True)
        hash_parser.add_argument('-i', '--input', required=True)
        
        # Base64命令
        base64_parser = subparsers.add_parser('base64', help='Base64编码/解码')
        base64_parser.add_argument('action', choices=['encode', 'decode'])
        base64_parser.add_argument('-i', '--input', required=True, help='输入文件路径')
        base64_parser.add_argument('-o', '--output', required=True, help='输出文件路径')
        
        # 密钥管理命令
        key_parser = subparsers.add_parser('key', help='密钥管理')
        key_parser.add_argument('action', choices=['generate', 'revoke', 'list'])
        key_parser.add_argument('-t', '--type', choices=['aes', 'rsa'], required=True)
        key_parser.add_argument('-i', '--id', help='密钥ID')
        
        return parser

    def run(self):
        try:
            args = self.parser.parse_args()
            
            if args.command == 'key':
                self._handle_key_command(args)
                return
                
            with open(args.input, 'rb') as f:
                data = f.read()
            
            if args.command == 'encrypt':
                if args.algo == 'hybrid' and not args.key_id:
                    print("错误: 混合加密需要指定密钥ID", file=sys.stderr)
                    sys.exit(1)
                    
                result = self.core.execute(
                    mode='encrypt',
                    algo=args.algo,
                    data=data,
                    key_id=args.key_id
                )
                
                with open(args.output, 'wb') as f:
                    f.write(result)
                print(f"加密完成，结果已保存到: {args.output}")
            
            elif args.command == 'decrypt':
                if args.algo == 'hybrid' and not args.key_id:
                    print("错误: 混合解密需要指定密钥ID", file=sys.stderr)
                    sys.exit(1)
                    
                result = self.core.execute(
                    mode='decrypt',
                    algo=args.algo,
                    data=data,
                    key_id=args.key_id
                )
                
                with open(args.output, 'wb') as f:
                    f.write(result)
                print(f"解密完成，结果已保存到: {args.output}")
            
            elif args.command == 'hash':
                digest = self.core.execute(
                    mode='hash',
                    algo=args.algo,
                    data=data
                )
                print(f"{args.algo}哈希值: {digest}")
            
            elif args.command == 'base64':
                if args.action == 'encode':
                    result = self.core.encode_base64(data)
                else:  # decode
                    result = self.core.decode_base64(data)
                
                with open(args.output, 'wb') as f:
                    f.write(result)
                print(f"Base64 {args.action}完成，结果已保存到: {args.output}")
            
        except FileNotFoundError:
            print(f"错误: 找不到文件 {args.input}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"错误: {str(e)}", file=sys.stderr)
            sys.exit(1)
        finally:
            if hasattr(self, 'core'):
                self.core.key_manager.close()

    def _handle_key_command(self, args):
        """处理密钥管理命令"""
        if args.action == 'generate':
            key_id = self.core.generate_key(args.type, key_id=args.id)
            print(f"生成的密钥ID: {key_id}")
        elif args.action == 'revoke':
            if not args.id:
                print("错误: 吊销密钥需要指定密钥ID", file=sys.stderr)
                sys.exit(1)
            self.core.revoke_key(args.id)
            print(f"已吊销密钥: {args.id}")
        elif args.action == 'list':
            # TODO: 实现密钥列表功能
            print("密钥列表功能待实现")

if __name__ == '__main__':
    CryptoCli().run()