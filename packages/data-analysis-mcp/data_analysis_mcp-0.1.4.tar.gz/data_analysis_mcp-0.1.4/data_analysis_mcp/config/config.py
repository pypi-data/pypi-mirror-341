import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

# 服务配置
DEBUG = os.environ.get("MCP_DEBUG", "False").lower() == "true"

# API配置
DATA_ANALYSIS_API_URL = os.environ.get(
    "DATA_ANALYSIS_API_URL", 
    "http://llmtest.ouyeelf.com/api/v1/process/8e874fc9-6782-4e4a-b589-21d2a71adfbb"
)

# OpenAI API配置
ASSISTANT_API_BASE = os.environ.get("ASSISTANT_API_BASE", "http://llmtest.ouyeelf.com/api/v2/assistant")
ASSISTANT_MODEL = os.environ.get("ASSISTANT_MODEL", "578751c7-377a-4669-ac57-accfbb1fe157")

# 日志配置
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' 