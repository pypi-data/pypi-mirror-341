"""
工具类模块，包含 AIVK 使用的通用工具函数和类
"""

import shlex
import subprocess
import asyncio
import logging
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
             log_level: int = logging.INFO
             ) -> Tuple[int, str, str]:
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

        Returns:
            返回值元组 (返回码, 标准输出, 标准错误)
        """
        logger = logging.getLogger(__name__)
        
        if isinstance(cmd, str) and not shell:
            cmd = shlex.split(cmd)
        
        logger.log(log_level, f"执行命令: {cmd}")
        
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
                   log_level: int = logging.INFO
                   ) -> Tuple[int, str, str]:
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

        Returns:
            返回值元组 (返回码, 标准输出, 标准错误)
        """
        logger = logging.getLogger(__name__)
        
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