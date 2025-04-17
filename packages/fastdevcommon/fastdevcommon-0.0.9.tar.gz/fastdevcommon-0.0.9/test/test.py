import asyncio
import sys
import os
import json
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from FastDevCommon._client.nacos.nacos_client import NacosClient
from FastDevCommon._client.nacos.client_config import NacosClientConfig
from FastDevCommon._client.http_client import HttpClient

async def discover_service(nacos_client: NacosClient, service_name: str, group_name: str = "DEFAULT_GROUP") -> Dict[str, Any]:
    """
    从Nacos发现服务实例

    Args:
        nacos_client: Nacos客户端
        service_name: 服务名称
        group_name: 服务分组

    Returns:
        Dict: 服务实例信息
    """
    print(f"正在查询服务: {service_name}")
    instances = await nacos_client.list_instances(service_name, group_name=group_name)
    print(2222,instances)
    if not instances or not instances.get('hosts') or len(instances.get('hosts')) == 0:
        print(f"未找到服务: {service_name}")
        return None

    # 选择第一个健康的实例
    healthy_instances = [instance for instance in instances.get('hosts', []) if instance.get('healthy', False)]

    if not healthy_instances:
        print(f"未找到健康的服务实例: {service_name}")
        return None

    instance = healthy_instances[0]
    print(f"找到服务实例: {instance.get('ip')}:{instance.get('port')}")
    return instance

async def call_service(instance: Dict[str, Any], path: str, method: str = "GET", data: Dict = None) -> Dict:
    """
    调用微服务接口

    Args:
        instance: 服务实例信息
        path: 接口路径
        method: HTTP方法
        data: 请求数据

    Returns:
        Dict: 响应数据
    """
    if not instance:
        return {"error": "服务实例不存在"}

    ip = instance.get('ip')
    port = instance.get('port')

    url = f"http://{ip}:{port}{path}"
    print(f"调用服务: {url}")

    client = HttpClient()
    headers = {
        "Content-Type": "application/json",
    }
    try:
        if method.upper() == "GET":
            response = await client.get(url, params=data)
        elif method.upper() == "POST":
            response = await client.post(url, json=data,headers=headers)
        elif method.upper() == "PUT":
            response = await client.put(url, data=data)
        elif method.upper() == "DELETE":
            response = await client.delete(url, data=data)
        else:
            return {"error": f"不支持的HTTP方法: {method}"}

        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except:
                return {"text": response.text}
        else:
            return {"error": f"请求失败，状态码: {response.status_code}", "text": response.text}
    except Exception as e:
        return {"error": f"请求异常: {str(e)}"}

async def test_call_service():
    """测试调用其他微服务"""
    # Nacos配置
    config = NacosClientConfig(
        server_address="http://127.0.0.1:8848",  # 修改为您的Nacos服务器地址
        namespace_id="public",                   # 修改为您的命名空间
        access_key="nacos",                      # 修改为您的用户名
        secret_key="nacos",                      # 修改为您的密码
        version="v1"                             # 使用v1或v2 API
    )

    # 创建Nacos客户端
    nacos_client = NacosClient.from_config(config)

    # 要调用的服务名称
    service_name = "jingxin-intelligence"  # 修改为您要调用的服务名称

    # 发现服务
    instance = await discover_service(nacos_client, service_name)
    if not instance:
        print(f"无法找到服务: {service_name}")
        return

    # # 调用服务的健康检查接口
    # health_result = await call_service(instance, "/actuator/health", "GET")
    # print(f"健康检查结果: {json.dumps(health_result, indent=2, ensure_ascii=False)}")
    #
    # # 调用服务的业务接口示例
    # api_result = await call_service(instance, "/api/example", "GET")
    # print(f"API调用结果: {json.dumps(api_result, indent=2, ensure_ascii=False)}")
    headers = {
        "Content-Type": "application/json",
    }
    order_data = {"intelligenceId": 297927865570299904}
    response = await nacos_client.post("jingxin-intelligence", "/intelligence/inner/getInfo", headers=headers,json=order_data)
    if response and response.ok:
        order_result = response.json()
        print(f"订单创建成功: {order_result}")
    else:
        print("创建订单失败")
    # post_data = {"intelligenceId": 297927865570299904}
    # post_result = await call_service(instance, "/intelligence/inner/getInfo", "POST", post_data)
    # print(f"POST调用结果: {json.dumps(post_result, indent=2, ensure_ascii=False)}")

async def main():
    """主函数"""
    print("开始测试调用其他微服务...")

    try:
        await test_call_service()
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

    print("测试完成")



if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())