"""
SDK配置文件
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from typing import Optional

def load_environment_variables() -> None:
    """加载环境变量文件"""
    # 尝试从多个可能的位置加载 .env 文件
    possible_env_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'),  # lqcode_sdk/.env
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'),  # 项目根目录/.env
    ]
    
    env_loaded = False
    for env_path in possible_env_paths:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            env_loaded = True
            break
    
    if not env_loaded:
        print("警告: 未找到 .env 文件，将使用默认值或系统环境变量")
    
    # 验证必要的环境变量
    required_vars = [
        'LQCODE_API_URL',
        'LQCODE_WORKFLOW_ID',
        'LQCODE_MAX_RETRIES',
        'LQCODE_BASE_DELAY',
        'LQCODE_TOKEN_EXPIRY_HOURS',
        'LQCODE_CACHE_SIZE'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"警告: 以下环境变量未设置: {', '.join(missing_vars)}")

# 加载环境变量
load_environment_variables()

@dataclass
class Config:
    """SDK配置类"""
    # API配置
    base_url: str = os.getenv('LQCODE_API_URL', '')
    workflow_id: str = os.getenv('LQCODE_WORKFLOW_ID', '')
    
    # 重试配置
    max_retries: int = int(os.getenv('LQCODE_MAX_RETRIES', '3'))
    base_delay: int = int(os.getenv('LQCODE_BASE_DELAY', '2'))
    
    # Token配置
    token_expiry_hours: int = int(os.getenv('LQCODE_TOKEN_EXPIRY_HOURS', '1'))
    cache_size: int = int(os.getenv('LQCODE_CACHE_SIZE', '100'))
    
    # 配置键列表
    CONFIG_KEYS = [
        'base_url',
        'workflow_id',
        'max_retries',
        'base_delay',
        'token_expiry_hours',
        'cache_size'
    ]
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> 'Config':
        """从字典创建配置实例"""
        return cls(**{k: v for k, v in config_dict.items() if k in cls.CONFIG_KEYS})
    
    def to_dict(self) -> dict:
        """将配置转换为字典"""
        return {k: getattr(self, k) for k in self.CONFIG_KEYS}
    
    def validate(self) -> bool:
        """验证配置是否有效"""
        if not self.base_url:
            print("错误: LQCODE_API_URL 未设置")
            return False
        if not self.workflow_id:
            print("错误: LQCODE_WORKFLOW_ID 未设置")
            return False
        return True 