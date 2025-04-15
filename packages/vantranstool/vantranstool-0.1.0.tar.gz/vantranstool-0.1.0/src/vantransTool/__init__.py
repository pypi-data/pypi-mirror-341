"""
vantransTool - 一个基于MCP协议的运输工具服务
提供批量外部派车功能
"""

from .client import dispatch_orders
from .config import *

__version__ = "0.1.0"
__all__ = [
    "dispatch_orders",
] 