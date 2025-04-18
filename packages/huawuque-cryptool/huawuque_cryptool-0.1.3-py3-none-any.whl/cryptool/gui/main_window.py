import sys
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__) # 获取 __main__ logger

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from cryptool.core.app import CryptoCore
import base64
import uuid
from typing import Optional

class CryptoGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        try:
            # 设置默认的分块大小（以字节为单位）
            self.block_size = tk.IntVar(value=4096)  # 默认4KB
            self.algo_var = tk.StringVar(value='aes')  # 默认AES算法
            
            # 创建可能在多个面板间共享的变量和控件
            self.key_entry_var = tk.StringVar(value="")  # 密钥ID变量
            
            self.core = CryptoCore()
            self.setup_window()
            self.setup_styles()
            
            # 创建主框架
            self.main_frame = ttk.Frame(self, padding="10", style='Main.TFrame')
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 左侧功能按钮区域
            self.button_frame = ttk.Frame(self.main_frame)
            self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
            
            # 右侧操作区域
            self.content_frame = ttk.Frame(self.main_frame)
            self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 创建功能按钮
            self._create_function_buttons()
            
            # 初始化日志内容列表
            self.log_messages = []
            
            # 默认显示算法选择界面
            self._show_algorithm_panel()
            
        except Exception as e:
            logger.error(f"初始化失败: {e}")
            messagebox.showerror("初始化错误", f"程序初始化失败: {str(e)}")
            self.destroy()
            sys.exit(1)
    #设置窗口基本属性
    def setup_window(self):
        """设置窗口基本属性"""
        self.title("加密工具")
        self.geometry("1000x800")
        self.minsize(800, 600)
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
    def setup_styles(self):
        """设置自定义样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义按钮样式
        style.configure(
            'Custom.TButton',
            padding=5,
            font=('微软雅黑', 10),
            background='#2E7D32',
            foreground='white'
        )
        
        # 自定义标签框样式
        style.configure(
            'Custom.TLabelframe',
            padding=10,
            font=('微软雅黑', 10),
            background='#BBDEFB',
            foreground='#0D47A1'
        )
        
        # 自定义标签样式
        style.configure(
            'Custom.TLabel',
            font=('微软雅黑', 10),
            background='#BBDEFB',
            foreground='#0D47A1'
        )
        
        # 自定义输入框样式
        style.configure(
            'Custom.TEntry',
            padding=5,
            fieldbackground='white',
            foreground='#0D47A1'
        )
        
        # 设置窗口背景色
        self.configure(bg='#BBDEFB')
        
        # 设置主框架背景色
        style.configure(
            'Main.TFrame',
            background='#BBDEFB'
        )
    def _create_function_buttons(self):
        """创建左侧功能按钮"""
        buttons = [
            ("算法选择", self._show_algorithm_panel),
            ("文件操作", self._show_file_panel),
            ("密钥管理", self._show_key_panel),
            ("加密/解密", self._show_operation_panel),
            ("高级设置", self._show_settings_panel),
            ("Base64工具", self._show_base64_panel),
            ("查看日志", self._show_log_window)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(
                self.button_frame,
                text=text,
                command=command,
                style='Custom.TButton',
                width=15
            )
            btn.pack(pady=5, fill=tk.X)
            
        # 在底部添加日志计数器
        frame = ttk.Frame(self.button_frame)
        frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.log_count = tk.IntVar(value=0)
        ttk.Label(
            frame,
            textvariable=self.log_count,
            style='Custom.TLabel'
        ).pack(side=tk.LEFT)
        
        ttk.Label(
            frame,
            text="条操作日志",
            style='Custom.TLabel'
        ).pack(side=tk.LEFT)
    
    def _clear_content_frame(self):
        """清空内容区域"""
        # 移除算法变量的跟踪
        try:
            if hasattr(self, 'algo_trace_id') and self.algo_trace_id:
                self.algo_var.trace_remove("write", self.algo_trace_id)
                self.algo_trace_id = None
        except (AttributeError, ValueError, TypeError):
            # 如果 trace_remove 方法不可用或参数不匹配，尝试使用旧版本的 trace_vdelete
            try:
                self.algo_var.trace_vdelete("w", self.algo_trace_id)
                self.algo_trace_id = None
            except Exception:
                # 忽略任何错误，确保程序可以继续运行
                pass
            
        # 清除对文本控件的引用
        if hasattr(self, 'desc_text'):
            del self.desc_text
            
        # 清空内容区域
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def _show_algorithm_panel(self):
        """显示算法选择面板"""
        self._clear_content_frame()
        
        frame = ttk.LabelFrame(
            self.content_frame,
            text="算法选择",
            style='Custom.TLabelframe'
        )
        frame.pack(fill=tk.X, pady=10, padx=10)
        
        algorithms = [
            ("AES 对称加密", 'aes'),
            ("RSA 非对称加密", 'rsa'),
            ("混合加密", 'hybrid')
        ]
        
        for text, value in algorithms:
            ttk.Radiobutton(
                frame,
                text=text,
                variable=self.algo_var,
                value=value,
                style='Custom.TRadiobutton'
            ).pack(anchor=tk.W, padx=20, pady=5)
            
        # 添加算法说明
        desc_frame = ttk.LabelFrame(
            self.content_frame,
            text="算法说明",
            style='Custom.TLabelframe' 
        )
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        descriptions = {
            'aes': "AES（高级加密标准）是一种对称加密算法，使用相同的密钥进行加密和解密。\n\n优点：加密速度快，适合大文件\n缺点：密钥分发困难",
            'rsa': "RSA是一种非对称加密算法，使用公钥加密，私钥解密。\n\n优点：密钥管理安全\n缺点：加密速度慢，不适合大文件",
            'hybrid': "混合加密结合了对称加密和非对称加密的优点。\n使用RSA加密会话密钥，再用会话密钥进行AES加密数据。\n\n优点：速度快且安全\n缺点：实现复杂"
        }
        
        text = tk.Text(
            desc_frame,
            height=10,
            wrap=tk.WORD,
            font=('微软雅黑', 10),
            bg='#E3F2FD',
            fg='#0D47A1'
        )
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 初始显示
        text.insert(tk.END, descriptions[self.algo_var.get()])
        
        # 保存对文本控件的引用
        self.desc_text = text
        
        # 创建一个新的回调函数变量
        self.algo_trace_id = None
        
        # 定义回调函数
        def update_description(*args):
            if hasattr(self, 'desc_text') and self.desc_text.winfo_exists():
                algo = self.algo_var.get()
                self.desc_text.delete(1.0, tk.END)
                self.desc_text.insert(tk.END, descriptions[algo])
        
        # 先移除任何现有的trace
        try:
            if self.algo_trace_id:
                self.algo_var.trace_remove("write", self.algo_trace_id)
        except (AttributeError, ValueError, TypeError):
            # 如果 trace_remove 方法不可用或参数不匹配，尝试使用旧版本的 trace_vdelete
            try:
                self.algo_var.trace_vdelete("w", self.algo_trace_id)
            except Exception:
                # 忽略任何错误，确保程序可以继续运行
                pass
        
        # 添加新的trace - 使用兼容旧版本的方式
        try:
            # 尝试使用新版本的 trace_add
            self.algo_trace_id = self.algo_var.trace_add("write", update_description)
        except (AttributeError, TypeError):
            # 回退到旧版本的 trace
            self.algo_trace_id = self.algo_var.trace("w", update_description)
    
    def _show_file_panel(self):
        """显示文件操作面板"""
        self._clear_content_frame()
        
        frame = ttk.LabelFrame(
            self.content_frame,
            text="文件操作",
            style='Custom.TLabelframe'
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # 创建输入文件选择区域
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            input_frame,
            text="输入文件:",
            style='Custom.TLabel',
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        self.input_label = ttk.Label(
            input_frame,
            text="未选择",
            style='Custom.TLabel'
        )
        self.input_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            input_frame,
            text="选择文件",
            command=self._load_input_file,
            style='Custom.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # 创建输出文件选择区域
        output_frame = ttk.Frame(frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            output_frame,
            text="输出文件:",
            style='Custom.TLabel',
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        self.output_label = ttk.Label(
            output_frame,
            text="未选择",
            style='Custom.TLabel'
        )
        self.output_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            output_frame,
            text="选择文件",
            command=self._load_output_file,
            style='Custom.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # 添加文件格式说明
        info_frame = ttk.LabelFrame(
            self.content_frame,
            text="文件操作说明",
            style='Custom.TLabelframe'
        )
        info_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(
            info_frame,
            text="· 加密操作需要选择输入文件（明文）和输出文件（密文）\n"
                 "· 解密操作需要选择输入文件（密文）和输出文件（明文）\n"
                 "· 支持任意格式的文件加密和解密\n"
                 "· 大文件加密时请在高级设置中调整分块大小",
            style='Custom.TLabel',
            justify=tk.LEFT
        ).pack(padx=10, pady=10, anchor=tk.W)
    
    def _show_key_panel(self):
        """显示密钥管理面板"""
        self._clear_content_frame()
        
        frame = ttk.LabelFrame(
            self.content_frame,
            text="密钥管理",
            style='Custom.TLabelframe'
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # 创建密钥ID输入区域
        key_input_frame = ttk.Frame(frame)
        key_input_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            key_input_frame,
            text="密钥ID:",
            style='Custom.TLabel',
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        self.key_entry = ttk.Entry(
            key_input_frame,
            style='Custom.TEntry',
            textvariable=self.key_entry_var  # 使用共享变量
        )
        self.key_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 创建密钥操作按钮区域
        key_btn_frame = ttk.Frame(frame)
        key_btn_frame.pack(pady=10)
        
        ttk.Button(
            key_btn_frame,
            text="生成新密钥",
            command=self._generate_key,
            style='Custom.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            key_btn_frame,
            text="吊销密钥",
            command=self._revoke_key,
            style='Custom.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        # 添加密钥说明
        info_frame = ttk.LabelFrame(
            self.content_frame,
            text="密钥管理说明",
            style='Custom.TLabelframe'
        )
        info_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(
            info_frame,
            text="· 不同算法需要生成对应的密钥类型\n"
                 "· AES算法使用对称密钥，长度为256位\n"
                 "· RSA算法自动生成公钥和私钥对\n"
                 "· 混合加密使用RSA加密的AES密钥\n"
                 "· 加密和解密时必须使用相同的密钥ID",
            style='Custom.TLabel',
            justify=tk.LEFT
        ).pack(padx=10, pady=10, anchor=tk.W)
    
    def _show_operation_panel(self):
        """显示加密/解密操作面板"""
        self._clear_content_frame()
        
        frame = ttk.LabelFrame(
            self.content_frame,
            text="加密/解密操作",
            style='Custom.TLabelframe'
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # 显示当前配置
        config_frame = ttk.Frame(frame)
        config_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            config_frame,
            text="当前配置:",
            style='Custom.TLabel'
        ).pack(side=tk.LEFT, padx=5)
        
        self.config_label = ttk.Label(
            config_frame,
            text="未设置完整参数",
            style='Custom.TLabel'
        )
        self.config_label.pack(side=tk.LEFT, padx=5)
        
        # 更新配置显示
        def update_config():
            algo = self.algo_var.get().upper()
            key_id = self.key_entry_var.get() or "未指定"
            input_file = getattr(self, 'input_file', "未选择")
            output_file = getattr(self, 'output_file', "未选择")
            block_size = self.block_size.get()
            
            if not hasattr(self, 'input_file') or not hasattr(self, 'output_file') or not self.key_entry_var.get():
                self.config_label.config(text="未设置完整参数")
            else:
                input_short = input_file.split('/')[-1] if '/' in input_file else input_file.split('\\')[-1]
                output_short = output_file.split('/')[-1] if '/' in output_file else output_file.split('\\')[-1]
                self.config_label.config(text=f"算法: {algo}, 密钥: {key_id}, 分块: {block_size}字节")
        
        update_config()
        
        # 创建操作按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(
            btn_frame,
            text="加密",
            command=lambda: self._on_encrypt(update_config),
            style='Custom.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame,
            text="解密",
            command=lambda: self._on_decrypt(update_config),
            style='Custom.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        # 添加操作步骤说明
        info_frame = ttk.LabelFrame(
            self.content_frame,
            text="操作步骤",
            style='Custom.TLabelframe'
        )
        info_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(
            info_frame,
            text="""1. 在"算法选择"中选择加密算法
2. 在"文件操作"中选择输入和输出文件
3. 在"密钥管理"中生成或指定密钥
4. 在"高级设置"中调整分块大小（可选）
5. 点击"加密"或"解密"按钮执行操作""",
            style='Custom.TLabel',
            justify=tk.LEFT
        ).pack(padx=10, pady=10, anchor=tk.W)
    
    def _show_settings_panel(self):
        """显示高级设置面板"""
        self._clear_content_frame()
        
        frame = ttk.LabelFrame(
            self.content_frame,
            text="高级设置",
            style='Custom.TLabelframe'
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # 分块大小设置
        block_frame = ttk.Frame(frame)
        block_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            block_frame,
            text="分块大小(字节):",
            style='Custom.TLabel'
        ).pack(side=tk.LEFT, padx=5)
        
        # 创建分块大小输入框
        self.block_size_entry = ttk.Entry(
            block_frame,
            width=15,
            style='Custom.TEntry',
            textvariable=self.block_size
        )
        self.block_size_entry.pack(side=tk.LEFT, padx=5)
        
        # 常用分块大小按钮
        sizes_frame = ttk.Frame(frame)
        sizes_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            sizes_frame,
            text="常用大小:",
            style='Custom.TLabel'
        ).pack(side=tk.LEFT, padx=5)
        
        # 添加一些常用的分块大小选项
        sizes = [
            ("1KB", 1024),
            ("4KB", 4096),
            ("16KB", 16384),
            ("64KB", 65536),
            ("1MB", 1048576)
        ]
        
        for text, value in sizes:
            ttk.Button(
                sizes_frame,
                text=text,
                command=lambda v=value: self._set_block_size(v),
                style='Custom.TButton'
            ).pack(side=tk.LEFT, padx=5)
        
        # 添加设置说明
        info_frame = ttk.LabelFrame(
            self.content_frame,
            text="设置说明",
            style='Custom.TLabelframe'
        )
        info_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(
            info_frame,
            text="· 分块大小影响加密/解密过程中的内存使用量和处理速度\n"
                 "· 较小的分块大小(如1KB)占用内存少，但处理速度可能较慢\n"
                 "· 较大的分块大小(如1MB)处理速度快，但占用更多内存\n"
                 "· 默认值4KB适合大多数场景\n"
                 "· 处理大文件(>100MB)时建议使用较大的分块大小\n"
                 "· 在内存受限设备上建议使用较小的分块大小",
            style='Custom.TLabel',
            justify=tk.LEFT
        ).pack(padx=10, pady=10, anchor=tk.W)
    
    def _show_base64_panel(self):
        """显示Base64工具面板"""
        self._clear_content_frame()
        
        frame = ttk.LabelFrame(
            self.content_frame,
            text="Base64编码/解码",
            style='Custom.TLabelframe'
        )
        frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # 文件选择
        file_frame = ttk.Frame(frame)
        file_frame.pack(fill=tk.X, pady=10)
        
        # 输入文件
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            input_frame,
            text="输入文件:",
            style='Custom.TLabel',
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        self.base64_input_label = ttk.Label(
            input_frame,
            text="未选择",
            style='Custom.TLabel'
        )
        self.base64_input_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            input_frame,
            text="选择文件",
            command=self._load_base64_input_file,
            style='Custom.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # 输出文件
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            output_frame,
            text="输出文件:",
            style='Custom.TLabel',
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        self.base64_output_label = ttk.Label(
            output_frame,
            text="未选择",
            style='Custom.TLabel'
        )
        self.base64_output_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(
            output_frame,
            text="选择文件",
            command=self._load_base64_output_file,
            style='Custom.TButton'
        ).pack(side=tk.RIGHT, padx=5)
        
        # 操作按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="编码文件",
            command=self._encode_base64_file,
            style='Custom.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame,
            text="解码文件",
            command=self._decode_base64_file,
            style='Custom.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        # 添加Base64说明
        info_frame = ttk.LabelFrame(
            self.content_frame,
            text="Base64说明",
            style='Custom.TLabelframe'
        )
        info_frame.pack(fill=tk.X, pady=10, padx=10)
        
        ttk.Label(
            info_frame,
            text="· Base64是一种将二进制数据转换为ASCII字符的编码方式\n"
                 "· 编码后的数据体积通常增加约33%\n"
                 "· 常用于在不支持二进制传输的媒介中传输二进制数据\n"
                 "· 适合在邮件、网页等文本环境中嵌入图片等二进制数据\n"
                 "· 注意：Base64不是加密算法，不提供安全保护",
            style='Custom.TLabel',
            justify=tk.LEFT
        ).pack(padx=10, pady=10, anchor=tk.W)

    def _show_log_window(self):
        """显示日志查看窗口"""
        # 创建一个新窗口
        log_window = tk.Toplevel(self)
        log_window.title("操作日志详情")
        log_window.geometry("800x600")
        log_window.minsize(600, 400)
        
        # 创建日志文本框和滚动条
        frame = ttk.Frame(log_window, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        log_text = tk.Text(
            frame,
            font=('Consolas', 10),
            yscrollcommand=scrollbar.set,
            bg='white',
            fg='#0D47A1',
            wrap=tk.WORD
        )
        log_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        scrollbar.config(command=log_text.yview)
        
        # 显示所有日志内容
        for message in self.log_messages:
            log_text.insert(tk.END, f"{message}\n")
        
        # 添加关闭按钮
        ttk.Button(
            log_window,
            text="关闭",
            command=log_window.destroy,
            style='Custom.TButton'
        ).pack(pady=10)
        
        # 滚动到最新日志
        log_text.see(tk.END)

    def log_message(self, message):
        """记录日志消息"""
        # 保存日志消息
        self.log_messages.append(message)
        
        # 更新日志计数
        self.log_count.set(len(self.log_messages))
        
        # 如果日志窗口已打开，也更新窗口内容
        for window in self.winfo_children():
            if isinstance(window, tk.Toplevel) and window.title() == "操作日志详情":
                for widget in window.winfo_children():
                    if isinstance(widget, ttk.Frame):
                        for child in widget.winfo_children():
                            if isinstance(child, tk.Text):
                                child.insert(tk.END, f"{message}\n")
                                child.see(tk.END)
                                break
    def _load_input_file(self):
        """选择输入文件"""
        self.input_file = filedialog.askopenfilename()
        if self.input_file:
            self.input_label.config(text=self.input_file)
            self.log_message(f"已选择输入文件: {self.input_file}")
    def _load_output_file(self):
        """选择输出文件"""
        self.output_file = filedialog.asksaveasfilename()
        if self.output_file:
            self.output_label.config(text=self.output_file)
            self.log_message(f"已选择输出文件: {self.output_file}")
    def _check_file_selection(self):
        """检查是否已选择输入和输出文件"""
        if not hasattr(self, 'input_file') or not hasattr(self, 'output_file'):
            messagebox.showwarning("警告", "请先选择输入和输出文件")
            return False
        return True
    def _on_encrypt(self, update_config=None):
        """处理加密操作"""
        if not self._check_file_selection():
            return
        try:
            with open(self.input_file, 'rb') as f:
                data = f.read()
            
            # 使用当前设置的分块大小
            block_size = self.block_size.get()
            
            result = self.core.execute(
                mode='encrypt',
                algo=self.algo_var.get(),
                data=data,
                key_id=self.key_entry_var.get() or None,  # 使用共享变量
                block_size=block_size  # 传递分块大小
            )
            
            with open(self.output_file, 'wb') as f:
                f.write(result)
            
            self.log_message(f"加密完成！结果已保存到: {self.output_file}")
            messagebox.showinfo("成功", f"文件加密成功！\n结果已保存到: {self.output_file}")
            
            # 如果提供了更新函数，调用它
            if update_config:
                update_config()
                
        except Exception as e:
            logger.error(f"加密失败: {e}")
            messagebox.showerror("错误", str(e))
    def _on_decrypt(self, update_config=None):
        """处理解密操作"""
        if not self._check_file_selection():
            return
        try:
            with open(self.input_file, 'rb') as f:
                data = f.read()
            
            # 使用当前设置的分块大小
            block_size = self.block_size.get()
            
            result = self.core.execute(
                mode='decrypt',
                algo=self.algo_var.get(),
                data=data,
                key_id=self.key_entry_var.get() or None,  # 使用共享变量
                block_size=block_size  # 传递分块大小
            )
            
            with open(self.output_file, 'wb') as f:
                f.write(result)
            
            self.log_message(f"解密完成！结果已保存到: {self.output_file}")
            messagebox.showinfo("成功", f"文件解密成功！\n结果已保存到: {self.output_file}")
            
            # 如果提供了更新函数，调用它
            if update_config:
                update_config()
                
        except Exception as e:
            logger.error(f"解密失败: {e}")
            messagebox.showerror("错误", str(e))
    def _generate_key(self):
        """生成新密钥"""
        try:
            algo_type = self.algo_var.get()
            key_id = self.core.generate_key(algo_type)
            key_id_str = str(key_id)  # 如果 key_id 是 None, 这里会变成 'None'
            self.key_entry_var.set(key_id_str)  # 使用共享变量
            self.log_message(f"已生成新的{algo_type.upper()}密钥: {key_id_str}")
            messagebox.showinfo("成功", f"已成功生成新的{algo_type.upper()}密钥: {key_id_str}")
        except Exception as e:
            # 记录更详细的错误，包括类型
            error_msg = f"生成密钥失败 ({type(e).__name__}): {str(e)}"
            logger.error(error_msg, exc_info=True) # 添加堆栈跟踪
            self.log_message(error_msg)
            messagebox.showerror("错误", error_msg)
    def _revoke_key(self):
        """吊销密钥"""
        key_id = self.key_entry_var.get()  # 使用共享变量
        if not key_id:
            messagebox.showwarning("警告", "请输入要吊销的密钥ID")
            return
        try:
            self.core.revoke_key(key_id)
            self.key_entry_var.set("")  # 使用共享变量
            self.log_message(f"密钥 {key_id} 已吊销")
            messagebox.showinfo("成功", f"密钥 {key_id} 已成功吊销")
        except Exception as e:
            logger.error(f"吊销密钥失败: {e}")
            messagebox.showerror("错误", f"吊销密钥失败: {str(e)}")
    def _load_base64_input_file(self):
        """加载Base64输入文件"""
        file_path = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[("所有文件", "*.*")]
        )
        if file_path:
            self.base64_input_label.config(text=file_path)
            self.log_message(f"已选择Base64输入文件: {file_path}")

    def _load_base64_output_file(self):
        """选择Base64输出文件"""
        file_path = filedialog.asksaveasfilename(
            title="选择输出文件",
            defaultextension=".b64",
            filetypes=[("Base64文件", "*.b64"), ("所有文件", "*.*")]
        )
        if file_path:
            self.base64_output_label.config(text=file_path)
            self.log_message(f"已选择Base64输出文件: {file_path}")

    def _encode_base64_file(self):
        """编码文件为Base64"""
        try:
            input_file = self.base64_input_label.cget("text")
            output_file = self.base64_output_label.cget("text")
            
            if input_file == "未选择" or output_file == "未选择":
                messagebox.showerror("错误", "请选择输入和输出文件")
                return
                
            with open(input_file, 'rb') as f:
                data = f.read()
                
            encoded_data = self.core.encode_base64(data)
            
            with open(output_file, 'wb') as f:
                f.write(encoded_data)
                
            self.log_message(f"文件已成功编码为Base64并保存到: {output_file}")
            messagebox.showinfo("成功", "文件编码完成")
            
        except Exception as e:
            self.log_message(f"Base64编码失败: {str(e)}")
            messagebox.showerror("错误", f"编码失败: {str(e)}")

    def _decode_base64_file(self):
        """解码Base64文件"""
        try:
            input_file = self.base64_input_label.cget("text")
            output_file = self.base64_output_label.cget("text")
            
            if input_file == "未选择" or output_file == "未选择":
                messagebox.showerror("错误", "请选择输入和输出文件")
                return
                
            with open(input_file, 'rb') as f:
                data = f.read()
                
            decoded_data = self.core.decode_base64(data)
            
            with open(output_file, 'wb') as f:
                f.write(decoded_data)
                
            self.log_message(f"Base64文件已成功解码并保存到: {output_file}")
            messagebox.showinfo("成功", "文件解码完成")
            
        except Exception as e:
            self.log_message(f"Base64解码失败: {str(e)}")
            messagebox.showerror("错误", f"解码失败: {str(e)}")
    def _on_closing(self):
        """窗口关闭时的清理工作"""
        try:
            if hasattr(self, 'core'):
                self.core.cleanup()
        except Exception as e:
            logger.error(f"关闭时出错: {e}")
        finally:
            self.destroy()
    def _set_block_size(self, size):
        """设置分块大小"""
        self.block_size.set(size)
        self.log_message(f"分块大小已设置为: {size} 字节")
def main():
    """程序入口点"""
    try:
        app = CryptoGUI()
        app.mainloop()
    except Exception as e:
        logger.critical(f"程序运行失败: {e}")
        sys.exit(1)
if __name__ == '__main__':
    main()