import asyncio
from data_analysis_mcp.services.data_analysis import DataAnalysisService
from data_analysis_mcp.utils.logger import setup_logging
setup_logging()

async def test():
    data_analysis_service = DataAnalysisService()
    result = await data_analysis_service.query_company_info("欧冶金服")
    return result

if __name__ == "__main__":
    # 使用asyncio运行协程
    asyncio.run(test())