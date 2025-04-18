import logging
import os
from pathlib import Path
import sys
import asyncio
from mcp.server.fastmcp import FastMCP
from data_analysis_mcp.config.config import DEBUG
from data_analysis_mcp.services.data_analysis import DataAnalysisService
from data_analysis_mcp.utils.logger import setup_logging

setup_logging()


# 设置日志
logger = logging.getLogger(__name__)

# 创建MCP服务器
app = FastMCP()

# 初始化服务
data_analysis_service = DataAnalysisService()


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
    logger.info(f"启动数据分析服务... ")
    app.run()

if __name__ == "__main__":
    main() 