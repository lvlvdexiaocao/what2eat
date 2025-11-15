"""
/src/core/config.py
用于放置核心文件
    -配置
"""
from functools import lru_cache
from typing import Literal

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """应用篇日志（支持postgreSQL和SQLite，含连接池设置"""

    app_name:str = "What to Eat"
    debug:bool = False

    # 数据库类型
    db_type: Literal["postgres", "sqlite"] = "sqlite"

    # postgreSQL配置
    db_host:str = "localhost"
    db_port:int = 5432
    db_user:str = "postgres"
    db_password:str = "postgres"
    db_name:str = "what2eat"

    # 连接池配置（仅PostgreSql有效）
    # --- 必选参数： 中等并发常用 ---
    pool_size:int = 20 # 连接池基础大小， 低 - ， 高 +
    max_overflow: int = 10 # 超出pool-四则的最大连接数
    pool_timeout: int = 30  # 获取连接超时事件s
    pool_pre_ping: bool = True  # 取消连接前是否检查可用性

    # --- 可选调优参数（高级场景） ---
    pool_recycle:int = 3600     # 连接最大存活事件s。避免长连接被数据库踢掉
    pool_use_lifo:bool = False  # 连接池取连接顺序，False=FIFO默认， TURE=LIFO，提高并发命中率
    echo:bool = False       # 是否终端打印SQL，开发可打开，生产关闭

    # SQLite配置
    sqlite_db_path:str="./data/what2eat.sqlite3"

    @computed_field
    @property
    def database_url(self)->str:
        if self.db_type == "postgres":
            return (
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        elif self.db_type == "sqlite":
            return f"sqlite+aiosqlite:///{self.sqlite_db_path}"

    @computed_field
    @property
    def engine_options(self)->dict:
        """统一封装 engine 欧赔ions， 供create_async_engine使用"""
        if self.db_type == "postgre":
            return {
                "pool_size":self.pool_size,
                "max_overflow":self.max_overflow,
                "pool_timeout":self.pool_timeout,
                "pool_use_lifo":self.pool_use_lifo,
                "echo":self.echo
            }
        # SQLite不支持pool设置，返回最小参数
        return {"echo":self.echo}

    # JWT配置
    jwt_secret:str = "lvlvdexiaocao"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False        # 大小写敏感
    )


# 缓存调用
# 小型项目暂时用不到
@lru_cache
def get_settings() ->Settings:
    return Settings()

settings = get_settings()

# settings = Settings()





















