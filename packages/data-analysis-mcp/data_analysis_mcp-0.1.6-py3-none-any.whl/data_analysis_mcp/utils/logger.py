import logging
from data_analysis_mcp.config.config import LOG_LEVEL, LOG_FORMAT

def setup_logger(name):
    """
    设置并返回一个配置好的日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        配置好的日志记录器
    """
    logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
    return logging.getLogger(name) 