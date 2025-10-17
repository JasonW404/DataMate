#!/usr/bin/env python3
"""
测试新的同步API接口
"""
import httpx
import json
from datetime import datetime

# API 基础URL
BASE_URL = "http://localhost:8000"

async def test_sync_api():
    """测试新的同步API"""
    
    # 测试数据
    test_data = {
        "mapping_id": "test-mapping-uuid-123",
        "batch_size": 10
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # 测试新的同步接口
            print("测试 POST /datasets/sync 接口...")
            response = await client.post(
                f"{BASE_URL}/datasets/sync",
                json=test_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                result = response.json()
                print("响应成功:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("响应错误:")
                print(response.text)
                
        except Exception as e:
            print(f"请求失败: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_sync_api())