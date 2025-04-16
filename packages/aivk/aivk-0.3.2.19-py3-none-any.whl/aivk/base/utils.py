"""
工具类模块，包含 AIVK 使用的通用工具函数和类
"""

import shlex
import subprocess
import asyncio
import logging
import os
import sys
import platform
import shutil
from pathlib import Path
from typing import List, Union, Dict, Tuple, Optional, Any

logger = logging.getLogger(__name__)
class AivkExecuter:
    """
    Aivk 命令执行器
    
    提供同步和异步执行系统命令的功能，支持超时设置、错误处理和命令输出捕获。
    """    
    
    @classmethod
    async def _exec(cls, cmd: str | list, cwd: str = None, shell: bool = False, env: dict = os.environ, 
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                   text: bool = True, encoding: str = 'utf-8', errors: str = 'replace'):
        """基础万能通用命令执行器（内部方法）
        
        简单高效的命令执行器，主要用于内部调用，不做过多的错误处理和安全检查。
        
        Args:
            cmd: 要执行的命令，可以是字符串或列表
            cwd: 工作目录
            shell: 是否使用shell执行
            env: 环境变量
            stdout: 标准输出处理方式，默认为PIPE
            stderr: 标准错误处理方式，默认为PIPE
            stdin: 标准输入处理方式，默认为PIPE
            text: 是否以文本模式返回输出
            encoding: 输出编码
            errors: 编码错误处理方式
            
        Returns:
            元组 (返回码, 标准输出, 标准错误)
        """
        # 处理命令参数
        if isinstance(cmd, list) and shell:
            cmd = " ".join(str(c) for c in cmd)
        elif isinstance(cmd, str) and not shell:
            cmd = shlex.split(cmd)
            
        # 创建进程
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            shell=shell,
            env=env,
            stdout=stdout,
            stderr=stderr,
            stdin=stdin,
            text=text,
            encoding=encoding,
            errors=errors,
            universal_newlines=text,
            bufsize=-1  # 系统默认缓冲
        )
        
        # 等待进程完成并获取输出
        stdout_data, stderr_data = await asyncio.get_event_loop().run_in_executor(
            None, process.communicate
        )
        
        # 返回结果
        return process.returncode, stdout_data, stderr_data

    @classmethod
    async def aexec(
        cls,
        cmd: str | list,
        cwd: str = None,
        terminal: str = None,  # 终端程序，Windows默认为wt (Windows Terminal)
        shell: str = None,     # shell类型，Windows默认为powershell
        **kwargs               # 其他自定义参数
    ):
        """异步命令执行器，支持自定义终端和shell

        Args:
            cmd: 要执行的命令，可以是字符串或列表
            cwd: 工作目录，默认为当前目录
            terminal: 终端程序名称，Windows默认为wt (Windows Terminal)，Linux/macOS自动检测
            shell: shell类型，Windows默认为powershell，Linux/macOS默认为bash
            **kwargs: 其他参数，包括:
                use_shell: bool = True,        # 是否使用shell模式
                encoding: str = 'utf-8',       # 输出编码
                timeout: float = None,         # 超时时间(秒)
                env: dict = None,              # 环境变量
                text: bool = True,             # 是否以文本模式返回输出
                detach: bool = False,          # 是否分离进程
                window_title: str = None,      # 窗口标题
                errors: str = 'replace',       # 编码错误处理
                startup_dir: str = None,       # 启动目录(优先级高于cwd)
                new_tab: bool = False,         # 使用新标签页(仅Windows Terminal)
                split: str = None,             # 分屏方向，'h'水平分屏，'v'垂直分屏(仅Windows Terminal)
                profile: str = None,           # 终端配置文件(仅Windows Terminal)
                wait: bool = True,             # 是否等待命令完成
                log: bool = True,              # 是否记录日志
                admin: bool = False,           # 是否以管理员权限运行

        Returns:
            tuple: (返回码, 标准输出, 标准错误)
            如果 detach=True，返回 subprocess.Popen 对象
        """
        # 系统平台检测
        is_windows = platform.system() == "Windows"
        is_macos = platform.system() == "Darwin"
        is_linux = platform.system() == "Linux"
        
        # 参数解析
        use_shell = kwargs.get('use_shell', True)
        encoding = kwargs.get('encoding', 'utf-8')
        timeout = kwargs.get('timeout', None)  # 目前仅解析，在_exec中使用
        env_vars = kwargs.get('env', None)
        text_mode = kwargs.get('text', True)
        detach_process = kwargs.get('detach', False)
        window_title = kwargs.get('window_title', None)
        error_mode = kwargs.get('errors', 'replace')
        startup_dir = kwargs.get('startup_dir', None) or cwd
        new_tab = kwargs.get('new_tab', False)
        split_pane = kwargs.get('split', None)
        terminal_profile = kwargs.get('profile', None)
        enable_log = kwargs.get('log', True)
        as_admin = kwargs.get('admin', False)
        
        # 默认终端和shell设置
        if terminal is None:
            if is_windows:
                # 检查Windows Terminal是否可用
                if shutil.which("wt"):
                    terminal = "wt"
                else:
                    terminal = "cmd"  # 回退到cmd
            elif is_macos:
                terminal = "Terminal.app"
            elif is_linux:
                # 尝试几个常见的Linux终端
                for term in ["gnome-terminal", "konsole", "xterm", "terminator"]:
                    if shutil.which(term):
                        terminal = term
                        break
                if terminal is None:
                    terminal = "xterm"  # 回退到xterm
        
        if shell is None:
            if is_windows:
                # 检查是否有PowerShell
                if shutil.which("pwsh"):
                    shell = "pwsh"  # PowerShell Core
                elif shutil.which("powershell"):
                    shell = "powershell"  # Windows PowerShell
                else:
                    shell = "cmd"  # 回退到cmd
            else:
                # Linux/macOS默认使用bash
                if shutil.which("bash"):
                    shell = "bash"
                else:
                    shell = "sh"
        
        if enable_log:
            logger.debug(f"异步执行命令: {cmd}")
            logger.debug(f"参数: 终端={terminal}, shell={shell}, 工作目录={startup_dir}")
        
        # 处理命令格式
        if isinstance(cmd, list):
            cmd_list = cmd
            cmd_str = " ".join(shlex.quote(str(part)) for part in cmd)
        else:
            cmd_str = cmd
            if not use_shell:
                cmd_list = shlex.split(cmd_str)
            else:
                cmd_list = cmd_str
        
        # 构建完整命令
        final_cmd = []
        
        # 特殊情况：分离进程或使用自定义终端
        if detach_process or terminal != "default":
            # Windows平台处理
            if is_windows:
                if terminal == "wt" and shutil.which("wt"):
                    final_cmd = ["wt"]
                    
                    # Windows Terminal 特殊参数
                    if window_title:
                        final_cmd.extend(["--title", window_title])
                    
                    if startup_dir:
                        final_cmd.extend(["-d", str(startup_dir)])
                    
                    if terminal_profile:
                        final_cmd.extend(["-p", terminal_profile])
                    
                    if new_tab:
                        final_cmd.append("nt")
                    
                    if split_pane:
                        if split_pane.lower() in ['h', 'horizontal']:
                            final_cmd.extend(["sp", "-H"])
                        elif split_pane.lower() in ['v', 'vertical']:
                            final_cmd.extend(["sp", "-V"])
                    
                    # 添加shell
                    if shell in ["powershell", "pwsh"]:
                        final_cmd.append(shell)
                        # PowerShell需要特殊处理命令
                        ps_cmd = f"& {{ Set-Location '{startup_dir}'; {cmd_str} }}"
                        final_cmd.append(ps_cmd)
                    elif shell == "cmd":
                        final_cmd.extend([shell, "/k", f"cd /d {startup_dir} & {cmd_str}"])
                    else:
                        # 其他shell直接添加
                        final_cmd.extend([shell, cmd_str])
                
                elif terminal == "cmd" or not shutil.which("wt"):
                    # 使用传统cmd窗口
                    if shell == "cmd":
                        final_cmd = ["start", "cmd", "/k"]
                        if window_title:
                            final_cmd[1:1] = [f'"{window_title}"']
                        final_cmd.append(f"cd /d {startup_dir} & {cmd_str}")
                    else:
                        # 使用PowerShell
                        final_cmd = ["start", shell]
                        if window_title:
                            final_cmd[1:1] = [f'"{window_title}"']
                        final_cmd.append(f"-NoExit -Command \"Set-Location '{startup_dir}'; {cmd_str}\"")
                    
                    use_shell = True  # start命令需要shell模式
            
            # macOS平台处理
            elif is_macos:
                if terminal == "Terminal.app":
                    applescript = f'''
                    tell application "Terminal"
                        activate
                        do script "cd '{startup_dir}' && {shell} -c '{cmd_str}'"
                    end tell
                    '''
                    final_cmd = ["osascript", "-e", applescript]
                elif terminal == "iTerm":
                    applescript = f'''
                    tell application "iTerm"
                        activate
                        set newWindow to (create window with default profile)
                        tell current session of newWindow
                            write text "cd '{startup_dir}' && {shell} -c '{cmd_str}'"
                        end tell
                    end tell
                    '''
                    final_cmd = ["osascript", "-e", applescript]
                else:
                    # 其他终端直接使用open命令
                    final_cmd = ["open", "-a", terminal, f"cd '{startup_dir}' && {shell} -c '{cmd_str}'"]
            
            # Linux平台处理
            elif is_linux:
                if terminal == "gnome-terminal":
                    final_cmd = [terminal, "--", shell, "-c", f"cd '{startup_dir}' && {cmd_str}; exec {shell}"]
                elif terminal in ["konsole", "terminator"]:
                    final_cmd = [terminal, "-e", f"{shell} -c \"cd '{startup_dir}' && {cmd_str}; exec {shell}\""]
                else:
                    # 默认xterm处理
                    final_cmd = [terminal, "-e", f"{shell} -c \"cd '{startup_dir}' && {cmd_str}; exec {shell}\""]
            
            # 创建分离进程
            if detach_process:
                try:
                    # 进程配置
                    kwargs = {
                        'cwd': startup_dir,
                        'env': env_vars,
                        'shell': use_shell,
                        'close_fds': True,
                        'start_new_session': True if not is_windows else False
                    }
                    
                    # Windows特殊处理
                    if is_windows:
                        # 如果需要管理员权限
                        if as_admin:
                            # 创建启动信息
                            startupinfo = subprocess.STARTUPINFO()
                            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                            startupinfo.wShowWindow = 1  # SW_NORMAL
                            
                            # 使用runas
                            if isinstance(final_cmd, list):
                                cmd_to_run = " ".join(final_cmd)
                            else:
                                cmd_to_run = final_cmd
                            
                            final_cmd = ["runas", "/user:Administrator", cmd_to_run]
                            use_shell = True
                            kwargs['startupinfo'] = startupinfo
                        else:
                            # 普通启动
                            if not (terminal == "wt" and shutil.which("wt")):
                                kwargs['creationflags'] = 0x00000010  # CREATE_NEW_CONSOLE
                    
                    # 启动进程
                    if enable_log:
                        logger.info(f"分离进程启动命令: {final_cmd}")
                    
                    # 执行命令
                    process = subprocess.Popen(final_cmd, **kwargs)
                    return process
                
                except Exception as e:
                    logger.error(f"分离进程启动失败: {e}")
                    return None
            
            # 直接使用内部执行器运行命令
            if enable_log:
                logger.info(f"使用特定终端执行命令: {final_cmd}")
            
            return await cls._exec(
                cmd=final_cmd, 
                cwd=startup_dir,
                shell=use_shell,
                env=env_vars,
                text=text_mode,
                encoding=encoding,
                errors=error_mode
            )
        
        # 普通命令执行
        else:
            # 直接使用内部执行器
            return await cls._exec(
                cmd=cmd_list if not use_shell else cmd_str, 
                cwd=startup_dir,
                shell=use_shell,
                env=env_vars,
                text=text_mode,
                encoding=encoding,
                errors=error_mode
            )

