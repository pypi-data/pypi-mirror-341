"""
vantransTool - 一个基于MCP协议的运输工具服务
提供批量外部派车功能
"""

from .server import (
    batch_external_dispatch,
    get_pending_dispatch_details,
    find_records_by_order_numbers,
    create_external_dispatch,
    main
)

__version__ = "0.1.0"
__all__ = [
    "batch_external_dispatch",
    "get_pending_dispatch_details",
    "find_records_by_order_numbers",
    "create_external_dispatch",
    "main"
] 