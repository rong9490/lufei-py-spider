from fastapi import APIRouter
from typing import Union, Optional

shop = APIRouter()

# 路径参数: param, 动态处理
# py 3.6 后类型声明

# 路由匹配, 从上到下, 优先匹配, 顺序很重要
# 路径参数
@shop.get("/food/{food_id}")
def shop_food(food_id: int):
    return {"shop": "food" + food_id}

# (更常用)查询参数 & 连接
@shop.get("/jobs")
def shop_food(kd: Union[str, None], xl: Optional[str] = None, gj = None):  # 有默认参数 / 必选
    return {"shop": "jobs_" + kd + xl + gj}


