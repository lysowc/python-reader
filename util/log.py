# log.py
import os
from typing import Dict, Optional, Any
from logging import Logger, getLogger, Formatter, StreamHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler

from config.logging import LogSettings

# 初始化配置
settings = LogSettings()

# 创建日志根目录
os.makedirs(settings.LOG_DIR, exist_ok=True)

# 自定义格式
_formatter = Formatter(
    fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class Log:
    _channels: Dict[str, Logger] = {}

    @classmethod
    def channel(cls, name: Optional[str] = None) -> Logger:
        """
        获取指定 channel 的日志实例
        如果未指定 name,使用默认 channel
        """
        name = name or settings.LOG_DEFAULT_CHANNEL

        if name in cls._channels:
            return cls._channels[name]

        # 创建 channel 目录
        channel_dir = os.path.join(settings.LOG_DIR, name)
        os.makedirs(channel_dir, exist_ok=True)

        # 日志文件路径
        log_file = os.path.join(channel_dir, f"{name}.log")

        # 创建 logger
        logger = getLogger(f"log.{name}")
        logger.setLevel("INFO")
        logger.propagate = False  # 防止重复输出

        # 避免重复添加 handler
        if logger.hasHandlers():
            logger.handlers.clear()

        # 文件 handler（并发安全）
        file_handler = ConcurrentRotatingFileHandler(
            filename=log_file,
            mode="a",
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding="utf-8"
        )
        file_handler.setFormatter(_formatter)
        logger.addHandler(file_handler)

        # 可选：添加控制台输出
        console_handler = StreamHandler()
        console_handler.setFormatter(_formatter)
        logger.addHandler(console_handler)

        cls._channels[name] = logger
        return logger

    def __getattr__(self, name: str) -> Any:
        """
        代理到默认 channel
        例如:Log.info(...) 等价于 Log.channel().info(...)
        """
        default_logger = self.channel()
        attr = getattr(default_logger, name)
        return attr