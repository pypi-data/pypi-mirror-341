import os
import logging
from datetime import datetime

def configure_logging():
    # 指定日志文件夹路径
    log_dir = 'logs'
    
    # 创建日志文件夹（如果它不存在）
    os.makedirs(log_dir, exist_ok=True)
    
    # 获取今天的日期，用于日志文件名
    today_date = datetime.now().date()
    
    # 配置日志记录
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(name)s - %(message)s',
        datefmt='%H:%M:%S',
        handlers=[
            logging.StreamHandler(),  # 输出到控制台
            logging.FileHandler(f'{log_dir}/{today_date}.log')  # 输出到文件
        ]
    )

# 调用函数以配置日志记录
configure_logging()
