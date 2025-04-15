import asyncio
import logging
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        logger.info("正在连接到服务器...")
        # 连接到服务器，设置超时时间为30秒
        async with sse_client("http://localhost:8000/sse", timeout=30) as (read_stream, write_stream):
            logger.info("成功建立SSE连接")
            
            # 创建客户端会话
            session = ClientSession(read_stream, write_stream)
            logger.info("创建客户端会话")
            
            # 初始化会话
            await session.initialize()
            logger.info("会话初始化完成")
            
            # 测试批量派车功能
            dispatch_groups = [
                {
                    "order_numbers": ["5000987906", "5000987907"],
                    "supplier_name": "上海乐增",
                    "dispatch_type": "提货"
                }
            ]
            
            logger.info(f"开始执行批量派车，订单组: {dispatch_groups}")
            # 调用批量派车工具，设置超时时间为60秒
            try:
                result = await asyncio.wait_for(
                    session.call_tool("batch_external_dispatch", dispatch_groups),
                    timeout=60
                )
                logger.info(f"批量派车结果: {result}")
            except asyncio.TimeoutError:
                logger.error("派车操作超时，请检查服务器状态")
            except Exception as e:
                logger.error(f"派车操作失败: {e}", exc_info=True)
            
    except ConnectionError as e:
        logger.error(f"连接错误: {e}")
    except Exception as e:
        logger.error(f"发生错误: {e}", exc_info=True)
    finally:
        logger.info("客户端会话结束")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("用户中断执行")
    except Exception as e:
        logger.error(f"程序执行出错: {e}", exc_info=True) 