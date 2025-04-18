from datetime import datetime
import logging
import os
from pathlib import Path
from data_analysis_mcp.config.config import LOG_LEVEL, LOG_FORMAT

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