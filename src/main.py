"""
src/main.py
主业务逻辑

健康检查，一个实例的端点
"""

from fastapi import FastAPI, Response, Depends
from src.core.config import get_settings,  Settings


app = FastAPI(description="FastAPI 练习项目实战")

# 路由引入
@app.get("/")
def read_root(
        # 使用FastAPI 的依赖注入系统来获取配置实例
        # FastAPI 会自动调用 get_settings(), 由于缓存的存在，这几乎没有开销
        settings:Settings = Depends(get_settings)
):
    """一个实例端点，演示如何访问配置"""
    return {
        "message":f"hello from the {settings.app_name}!",
        # 演示如何使用在模型中动态计算的属性
        "database_url": settings.database_url,
        "jwt_secret":settings.jwt_secret
    }

@app.get("/health")
async def health_check(response:Response):
    response.status_code = 200
    return {"status":"ok!!!!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app")