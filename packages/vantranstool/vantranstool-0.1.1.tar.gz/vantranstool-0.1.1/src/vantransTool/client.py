import asyncio
import logging
import argparse
from typing import List, Dict
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def dispatch_orders(dispatch_groups: List[Dict], server_url: str = "http://localhost:8000/sse", timeout: int = 60) -> Dict:
    """
    批量派车函数
    :param dispatch_groups: 派车组列表
    :param server_url: 服务器URL
    :param timeout: 超时时间（秒）
    :return: 处理结果
    """
    try:
        logger.info("正在连接到服务器...")
        async with sse_client(server_url, timeout=30) as (read_stream, write_stream):
            logger.info("成功建立SSE连接")
            
            session = ClientSession(read_stream, write_stream)
            logger.info("创建客户端会话")
            
            await session.initialize()
            logger.info("会话初始化完成")
            
            logger.info(f"开始执行批量派车，订单组: {dispatch_groups}")
            try:
                result = await asyncio.wait_for(
                    session.call_tool("batch_external_dispatch", dispatch_groups),
                    timeout=timeout
                )
                logger.info(f"批量派车结果: {result}")
                return result
            except asyncio.TimeoutError:
                error_msg = "派车操作超时，请检查服务器状态"
                logger.error(error_msg)
                return {
                    "success": False,
                    "message": error_msg,
                    "success_count": 0,
                    "failed_groups": dispatch_groups
                }
            except Exception as e:
                error_msg = f"派车操作失败: {str(e)}"
                logger.error(error_msg, exc_info=True)
                return {
                    "success": False,
                    "message": error_msg,
                    "success_count": 0,
                    "failed_groups": dispatch_groups
                }
            
    except ConnectionError as e:
        error_msg = f"连接错误: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "message": error_msg,
            "success_count": 0,
            "failed_groups": dispatch_groups
        }
    except Exception as e:
        error_msg = f"发生错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "success": False,
            "message": error_msg,
            "success_count": 0,
            "failed_groups": dispatch_groups
        }
    finally:
        logger.info("客户端会话结束")

def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description="vantransTool 客户端")
    parser.add_argument("--server", default="http://localhost:8000/sse", help="服务器URL")
    parser.add_argument("--timeout", type=int, default=60, help="超时时间（秒）")
    parser.add_argument("--order-numbers", nargs="+", required=True, help="订单号列表")
    parser.add_argument("--supplier", required=True, help="供应商名称")
    parser.add_argument("--dispatch-type", choices=["提货", "送货", "干线"], required=True, help="派车类型")
    
    args = parser.parse_args()
    
    dispatch_groups = [{
        "order_numbers": args.order_numbers,
        "supplier_name": args.supplier,
        "dispatch_type": args.dispatch_type
    }]
    
    result = asyncio.run(dispatch_orders(dispatch_groups, args.server, args.timeout))
    print(result)

if __name__ == "__main__":
    main() 