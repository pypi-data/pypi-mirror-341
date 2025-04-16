"""
工具类模块，包含 AIVK 使用的通用工具函数和类
"""

import shlex
import subprocess
import asyncio
import logging
import os
import sys
from typing import List, Union, Dict, Tuple, Optional, Any


class AivkExecuter:
    """
    全能命令执行器
    
    提供同步和异步执行系统命令的功能，支持超时设置、错误处理和命令输出捕获。
    """    
    
    @classmethod
    def exec(cls, 
             cmd: Union[str, List[str]], 
             cwd: Optional[str] = None,
             env: Optional[Dict[str, str]] = None,
             timeout: Optional[float] = None,
             shell: bool = False,
             capture_output: bool = True,
             encoding: str = 'utf-8',
             check: bool = False,
             log_level: int = logging.INFO,
             detach: bool = False,
             new_window: bool = False,
             window_title: Optional[str] = None
             ) -> Union[Tuple[int, str, str], Optional[subprocess.Popen]]:
        """
        同步执行命令

        Args:
            cmd: 要执行的命令，可以是字符串或字符串列表
            cwd: 工作目录
            env: 环境变量
            timeout: 超时时间（秒）
            shell: 是否使用shell执行
            capture_output: 是否捕获输出
            encoding: 输出编码
            check: 命令失败时是否抛出异常
            log_level: 日志级别
            detach: 是否分离进程（不等待完成）
            new_window: 是否在新窗口中启动（要求detach=True）
            window_title: 窗口标题（仅Windows有效，要求new_window=True）

        Returns:
            正常执行返回元组 (返回码, 标准输出, 标准错误)
            detach=True时返回进程对象或None（出错时）
        """
        logger = logging.getLogger(__name__)
        
        if isinstance(cmd, str) and not shell:
            cmd = shlex.split(cmd)
        
        logger.log(log_level, f"执行命令: {cmd}")
        
        # 如果要求分离进程或启动新窗口，则使用Popen直接启动
        if detach or new_window:
            try:
                kwargs = {
                    'cwd': cwd,
                    'env': env,
                    'shell': shell,
                    'close_fds': True,
                    'start_new_session': True if sys.platform != 'win32' else False
                }
                
                if sys.platform == 'win32' and new_window:
                    # Windows系统特有配置
                    # 定义Windows常量
                    CREATE_NEW_CONSOLE = 0x00000010
                    STARTF_USESHOWWINDOW = 0x00000001
                    SW_NORMAL = 1
                    
                    # 设置启动参数
                    startupinfo = subprocess.STARTUPINFO()
                    
                    kwargs['creationflags'] = CREATE_NEW_CONSOLE
                    startupinfo.dwFlags |= STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = SW_NORMAL
                    kwargs['startupinfo'] = startupinfo
                    
                    # 如果指定了窗口标题，需要额外处理
                    if window_title:
                        # 需要通过批处理或PowerShell设置标题
                        if shell:
                            if isinstance(cmd, list):
                                cmd = " ".join(cmd)
                            cmd = f'start "{window_title}" /D "{cwd or os.getcwd()}" {cmd}'
                        else:
                            # 使用cmd.exe启动并设置标题
                            cmd_str = cmd if isinstance(cmd, str) else " ".join(f'"{arg}"' for arg in cmd)
                            cmd = ['cmd.exe', '/c', f'start "{window_title}" {cmd_str}']
                            shell = True
                            # 重新配置启动参数
                            kwargs.pop('creationflags', None)
                            kwargs.pop('startupinfo', None)
                elif new_window:
                    # Unix系统（Linux/macOS）
                    if sys.platform == 'darwin':  # macOS
                        # 使用open -a Terminal命令打开新终端
                        if isinstance(cmd, list):
                            cmd_str = " ".join(f"'{arg}'" for arg in cmd)
                        else:
                            cmd_str = cmd
                        cmd = ['open', '-a', 'Terminal', cmd_str]
                    else:  # Linux
                        # 尝试使用常见的终端模拟器
                        terminal_emulators = ['gnome-terminal', 'xterm', 'konsole', 'terminator']
                        terminal = None
                        
                        # 查找可用终端模拟器
                        for emulator in terminal_emulators:
                            try:
                                if subprocess.run(['which', emulator], 
                                                capture_output=True).returncode == 0:
                                    terminal = emulator
                                    break
                            except:
                                continue
                        
                        if terminal:
                            orig_cmd = cmd
                            if terminal == 'gnome-terminal':
                                if isinstance(orig_cmd, list):
                                    cmd_str = " ".join(f"'{arg}'" for arg in orig_cmd)
                                else:
                                    cmd_str = orig_cmd
                                cmd = [terminal, '--', 'bash', '-c', cmd_str]
                            else:
                                if isinstance(orig_cmd, list):
                                    cmd_str = " ".join(f"'{arg}'" for arg in orig_cmd)
                                else:
                                    cmd_str = orig_cmd
                                cmd = [terminal, '-e', f"bash -c '{cmd_str}'"]
                
                # 启动进程
                process = subprocess.Popen(cmd, **kwargs)
                return process
                
            except Exception as e:
                logger.error(f"启动程序异常: {e}")
                return None
        
        # 正常执行命令
        try:
            if capture_output:
                result = subprocess.run(
                    cmd, 
                    cwd=cwd,
                    env=env,
                    timeout=timeout,
                    shell=shell,
                    check=check,
                    text=True,
                    encoding=encoding,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return result.returncode, result.stdout, result.stderr
            else:
                result = subprocess.run(
                    cmd, 
                    cwd=cwd,
                    env=env,
                    timeout=timeout,
                    shell=shell,
                    check=check
                )
                return result.returncode, "", ""
        except subprocess.TimeoutExpired as e:
            logger.error(f"命令执行超时: {e}")
            return -1, "", f"命令执行超时: {e}"
        except subprocess.CalledProcessError as e:
            logger.error(f"命令执行失败: {e}")
            if check:
                raise
            return e.returncode, e.stdout or "", e.stderr or ""
        except Exception as e:
            logger.error(f"命令执行异常: {e}")
            if check:
                raise
            return -1, "", str(e)
    
    @classmethod
    async def aexec(cls, 
                   cmd: Union[str, List[str]], 
                   cwd: Optional[str] = None,
                   env: Optional[Dict[str, str]] = None,
                   timeout: Optional[float] = None,
                   shell: bool = False,
                   encoding: str = 'utf-8',
                   log_level: int = logging.INFO,
                   detach: bool = False,
                   new_window: bool = False,
                   window_title: Optional[str] = None
                   ) -> Union[Tuple[int, str, str], Optional[subprocess.Popen]]:
        """
        异步执行命令

        Args:
            cmd: 要执行的命令，可以是字符串或字符串列表
            cwd: 工作目录
            env: 环境变量
            timeout: 超时时间（秒）
            shell: 是否使用shell执行
            encoding: 输出编码
            log_level: 日志级别
            detach: 是否分离进程（不等待完成）
            new_window: 是否在新窗口中启动（要求detach=True）
            window_title: 窗口标题（仅Windows有效，要求new_window=True）

        Returns:
            正常执行返回元组 (返回码, 标准输出, 标准错误)
            detach=True时返回进程对象或None（出错时）
        """
        logger = logging.getLogger(__name__)
        
        # 如果要求分离进程，则直接使用同步方法启动
        if detach or new_window:
            return cls.exec(
                cmd=cmd,
                cwd=cwd,
                env=env,
                shell=shell,
                log_level=log_level,
                detach=True,
                new_window=new_window,
                window_title=window_title
            )
        
        # 正常异步执行
        if isinstance(cmd, str) and not shell:
            cmd = shlex.split(cmd)
        
        logger.log(log_level, f"异步执行命令: {cmd}")
        
        try:
            process = await asyncio.create_subprocess_shell(
                cmd if shell and isinstance(cmd, str) else " ".join(cmd) if shell else cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=env,
                shell=shell
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                stdout_str = stdout.decode(encoding) if stdout else ""
                stderr_str = stderr.decode(encoding) if stderr else ""
                
                return process.returncode or 0, stdout_str, stderr_str
            except asyncio.TimeoutError:
                try:
                    process.kill()
                except:
                    pass
                logger.error(f"异步命令执行超时")
                return -1, "", "命令执行超时"
        except Exception as e:
            logger.error(f"异步命令执行异常: {e}")
            return -1, "", str(e)