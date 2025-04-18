import datetime
import logging
import os
from pathlib import Path
import sys
import asyncio
from mcp.server.fastmcp import FastMCP
from data_analysis_mcp.config.config import DEBUG
from data_analysis_mcp.services.data_analysis import DataAnalysisService
from data_analysis_mcp.utils.logger import setup_logger
from datetime import datetime


# 设置日志
logger = setup_logger(__name__)

# 创建MCP服务器
app = FastMCP()

# 初始化服务
data_analysis_service = DataAnalysisService()
def setup_logging(log_dir: str = "logs") -> str:
    """Setup logging configuration and return log file path."""
    # Create log directory
    log_dir_path = Path(log_dir)
    log_dir_path.mkdir(exist_ok=True)
    
    # Create log file with timestamp
    log_file = log_dir_path / f"data_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Set log level from environment variable or default to INFO
    log_level_str = os.getenv("LOG_LEVEL", "INFO")
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # Print log file path
    print(f"Log file path: {log_file.absolute()}")
    
    return str(log_file)

@app.tool()
async def analyze_data(query: str) -> dict:
    """分析公司算账经营数据并生成报告
    
    Args:
        query: 用户的查询内容，例如"请分析1-6月份边际贡献最高的5家分公司"或"2024年6月通宝产品的信息化成本是多少"
    
    Returns:
        包含分析结果的JSON对象
    """
    logger.info(f"接收到数据分析查询: {query}")
    result = await data_analysis_service.analyze_data(query)
    return result

@app.tool()
async def query_company_info(query: str) -> str:
    """查询公司信息
    
    Args:
        query: 用户的查询内容，例如"欧冶金诚服务有限公司"
    
    Returns:
        公司相关信息的回答
    """
    logger.info(f"接收到公司信息查询: {query}")
    result = await data_analysis_service.query_company_info(query)
    return result

def main():
    """主函数"""
    setup_logging()
    logger.info(f"启动数据分析服务... ")
    app.run()

if __name__ == "__main__":
    main() 