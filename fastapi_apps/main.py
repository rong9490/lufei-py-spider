# AGSI服务器协议, Uvicorn
# py > 3.6

# python3 -m uvicorn main:app --reload

from fastapi import FastAPI
import uvicorn
from app01.urls import shop
from app02.urls import user

app = FastAPI()
app.include_router(shop, prefix="/shop", tags=["购物接口"])
app.include_router(user, prefix="/user", tags=["用户接口"])

# 路由映射函数的机制

# 异步函数

# 装饰器
@app.get("/")
async def home():
    return {"user_id": 1001} # 字节流 --> json --> http结构

@app.get("/shop")
def shop():
    return "shopping..."

if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)

# 子应用 解耦分发
# app.include_router()
# 分别有自身的 urls / routes
# 前缀、tags