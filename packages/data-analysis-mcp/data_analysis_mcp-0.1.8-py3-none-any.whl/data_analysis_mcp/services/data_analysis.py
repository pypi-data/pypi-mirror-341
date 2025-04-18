import json
import traceback
import aiohttp
import requests
from data_analysis_mcp.config.config import (
    DATA_ANALYSIS_API_URL,
    ASSISTANT_API_BASE,
    ASSISTANT_MODEL
)
import logging

logger = logging.getLogger(__name__)

class DataAnalysisService:
    """数据分析服务类"""
    
    def __init__(self):
        self.data_analysis_api_url = DATA_ANALYSIS_API_URL
        self.assistant_api_base = ASSISTANT_API_BASE
        self.assistant_model = ASSISTANT_MODEL
        logger.info("数据分析服务初始化完成")

    async def analyze_data(self, query):
        """
        分析数据并返回结果
        
        Args:
            query: 用户查询
            
        Returns:
            分析结果
        """
        logger.info(f"接收到数据分析查询: {query}")
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Content-Type": "application/json"
            }
            
            # 构建请求数据
            data = {
                "inputs": {
                    "question": "",
                    "input": query,
                    "id": "StructuredChatAgent-9b44c"
                },
                "tweaks": {
                    "GptsToolWrapper-2da13": {},
                    "BishengLLM-5ce00": {},
                    "GptsToolWrapper-0f494": {},
                    "StructuredChatAgent-9b44c": {},
                    "ConversationBufferMemory-eedfe": {}
                }
            }
            
            try:
                logger.info(f"发送请求到API: {self.data_analysis_api_url}")
                async with session.post(self.data_analysis_api_url, headers=headers, json=data) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"API请求失败，状态码: {response.status}, 错误: {error_text}")
                        return {
                            "status": "error",
                            "message": f"API请求失败，状态码: {response.status}",
                            "data": None
                        }
                    
                    # 处理响应
                    response_json = await response.json()
                    logger.info(f"API响应状态: {response_json.get('status_code')} - {response_json.get('status_message')}")
                    
                    # 提取分析结果
                    if response_json.get('status_code') == 200 and 'data' in response_json:
                        if 'result' in response_json['data']:
                            # 从output字段获取结果
                            if 'output' in response_json['data']['result']:
                                analysis_result = response_json['data']['result']['output']
                                logger.info(f"成功获取分析结果，长度: {len(analysis_result)}")
                                return {
                                    "status": "success",
                                    "message": "数据分析完成",
                                    "data": analysis_result
                                }
                            # 如果没有output字段，尝试从result字段获取
                            elif 'result' in response_json['data']['result']:
                                analysis_result = response_json['data']['result']['result']
                                logger.info(f"从result字段获取分析结果，长度: {len(analysis_result)}")
                                return {
                                    "status": "success",
                                    "message": "数据分析完成",
                                    "data": analysis_result
                                }
                            else:
                                logger.error("响应中未找到分析结果")
                                return {
                                    "status": "error",
                                    "message": "响应中未找到分析结果",
                                    "data": None
                                }
                        else:
                            logger.error("响应中未找到result字段")
                            return {
                                "status": "error",
                                "message": "响应中未找到result字段",
                                "data": None
                            }
                    else:
                        logger.error(f"API请求未成功: {response_json.get('status_message')}")
                        return {
                            "status": "error",
                            "message": f"API请求未成功: {response_json.get('status_message')}",
                            "data": None
                        }
            
            except Exception as e:
                logger.error(f"调用API时发生错误: {str(e)}")
                return {
                    "status": "error",
                    "message": f"调用API时发生错误: {str(e)}",
                    "data": None
                }

    async def query_company_info(self, query):
        """
        查询公司信息 (支持流式/非流式混合处理)
        
        Args:
            query: 用户查询 (支持简写如 "腾讯"，会自动补全为正式查询)
            
        Returns:
            str: 公司信息查询结果 或 错误提示
        """
        logger.info(f"Received company info query: {query}")

        # 智能补全查询语句
        need_completion = not any(kw in query for kw in ("公司", "企业", "信息"))
        if need_completion:
            query = f"请详细介绍{query}的公司信息，包括主营业务、成立时间和行业地位"
            logger.info(f"Optimized query: {query}")

        data = {
            "model": self.assistant_model,
            "messages": [{"role": "user", "content": query}],
            "temperature": 0.3,  # 适当增加多样性
            "stream": False  # 明确使用非流式模式
        }

        api_url = f"{self.assistant_api_base}/chat/completions"
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                logger.debug(f"Requesting API: {api_url}")
                async with session.post(api_url, json=data) as response:
                    # 处理 HTTP 错误
                    if response.status != 200:
                        error_detail = await response.text()
                        logger.error(f"API Error [{response.status}]: {error_detail[:200]}")
                        return f"请求失败，服务暂时不可用 (错误代码 {response.status})"

                    # 解析 JSON 响应
                    try:
                        response_json = await response.json()
                        logger.debug(f"Raw API response: {json.dumps(response_json, ensure_ascii=False)[:200]}...")
                    except json.JSONDecodeError as e:
                        logger.error(f"Invalid JSON response: {e}")
                        return "服务器返回了无效的响应格式"

                    # 提取响应内容
                    if response_json.get("choices"):
                        first_choice = response_json["choices"][0]
                        if "message" in first_choice:
                            return first_choice["message"].get("content", "未找到有效信息")
                    
                    logger.warning("Unexpected API response structure")
                    return "服务器返回了意外的响应格式"

        except aiohttp.ClientError as e:
            logger.error(f"Network error: {str(e)}")
            return "网络连接异常，请稍后重试"
        except Exception as e:
            logger.critical(f"Unexpected error: {traceback.format_exc()}")
            return f"系统错误: {str(e)}"
            
