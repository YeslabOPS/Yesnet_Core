import httpx
from fastapi import FastAPI
from pydantic import BaseModel

# 定义数据模型
class DataModel(BaseModel):
    rx: int

# 创建FastAPI应用
app = FastAPI()

# 缓存接收到的数据
data_cache = []

# 定义接收数据的接口
@app.post("/api/data")
async def receive_data(data: DataModel):
    # 将数据添加到缓存
    data_cache.append(data.rx)
    
    # 如果缓存中有10个数据，计算平均值并发送到AI微服务
    if len(data_cache) >= 10:
        average_value = sum(data_cache) / len(data_cache)
        await send_to_ai_service(average_value)
        data_cache.clear()  # 清空缓存

    return {"message": "Data received", "data": data}

# 发送数据到AI微服务
async def send_to_ai_service(average_value: float):
    #print(f"Sending average value to AI service: {average_value}")
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:50000/api/ai", json={"average_rx": average_value})
        return response.json() 