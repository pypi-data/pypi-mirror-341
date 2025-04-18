import unittest
import asyncio
from unittest.mock import patch, MagicMock
from data_analysis_mcp.services.data_analysis import DataAnalysisService

class TestDataAnalysisService(unittest.TestCase):
    """数据分析服务测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.service = DataAnalysisService()
    
    @patch('aiohttp.ClientSession.post')
    def test_analyze_data(self, mock_post):
        """测试数据分析功能"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = MagicMock(return_value={
            'status_code': 200,
            'data': {
                'result': {
                    'output': '测试分析结果'
                }
            }
        })
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # 执行测试
        result = asyncio.run(self.service.analyze_data("测试查询"))
        
        # 验证结果
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['data'], '测试分析结果')
    
    @patch('aiohttp.ClientSession.post')
    def test_query_company_info(self, mock_post):
        """测试公司信息查询功能"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status = 200
        
        # 模拟流式响应
        mock_content = MagicMock()
        mock_content.__aiter__.return_value = [
            b'data: {"choices":[{"delta":{"content":"test"}}]}',
            b'data: {"choices":[{"delta":{"content":"company"}}]}',
            b'data: {"choices":[{"delta":{"content":"info"}}]}'
        ]
        mock_response.content = mock_content
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # 执行测试
        result = asyncio.run(self.service.query_company_info("测试公司"))
        
        # 验证结果
        self.assertEqual(result, "testcompanyinfo")

if __name__ == '__main__':
    unittest.main() 