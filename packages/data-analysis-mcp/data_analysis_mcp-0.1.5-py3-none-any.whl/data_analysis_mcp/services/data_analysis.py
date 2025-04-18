import json
import aiohttp
import requests
from data_analysis_mcp.config.config import (
    DATA_ANALYSIS_API_URL,
    ASSISTANT_API_BASE,
    ASSISTANT_MODEL
)
from data_analysis_mcp.utils.logger import setup_logger

logger = setup_logger(__name__)

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
        查询公司信息
        
        Args:
            query: 用户查询
            
        Returns:
            公司信息查询结果
        """
        logger.info(f"接收到公司信息查询: {query}")
        
        # 确保查询内容包含公司名称
        if "公司" not in query and "企业" not in query and "信息" not in query:
            query = f"请介绍一下{query}公司的企业信息"
        
        logger.info(f"处理后的查询: {query}")
        
            
        data  = json.dumps({
            "model": self.assistant_model,
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": 0,
            "stream": False
            })
        
        api_url = f"{self.assistant_api_base}/chat/completions"
        async with aiohttp.ClientSession() as session:
        
            try:
                print(f"发送请求到API: {api_url}")
                async with session.post(api_url, json=data) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"API请求失败，状态码: {response.status}, 错误: {error_text}")
                        return f"API请求失败，状态码: {response.status}"
                    
                    # 处理流式响应
                    full_response = ""
                    print("开始接收流式响应...")
                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith("data: "):
                            try:
                                json_data = json.loads(line[6:])  # 去掉 "data: " 前缀
                                if json_data.get("choices") and json_data["choices"][0].get("delta"):
                                    delta = json_data["choices"][0]["delta"]
                                    if delta.get("content"):
                                        content = delta["content"]
                                        full_response += content
                                        print(f"接收到内容片段: {content[:20]}..." if len(content) > 20 else f"接收到内容片段: {content}")
                            except json.JSONDecodeError as e:
                                print(f"JSON解析错误: {e}, 行内容: {line[:50]}...")
                    
                    print(f"完整响应长度: {len(full_response)}")
                    return full_response
            
            except Exception as e:
                print(f"调用API时发生错误: {str(e)}")
                return f"调用API时发生错误: {str(e)}"
            
