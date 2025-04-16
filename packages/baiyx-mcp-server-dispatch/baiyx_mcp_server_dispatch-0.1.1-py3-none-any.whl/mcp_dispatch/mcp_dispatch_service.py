from mcp.server.fastmcp import FastMCP
from typing import List, Dict, Tuple
import requests
import json
import os

# 创建MCP服务实例
mcp = FastMCP("dispatch-mcp-server", log_level="INFO")

# 缓存文件路径
CACHE_FILE = "table_fields_cache.json"
RECORD_CACHE_FILE = "record_cache.json"

# 表ID配置
SUPPLIER_DISPATCH_TABLE = "dst4wWd4usqcuQ0K2i"  # 供应商派车表
GOODS_DETAIL_TABLE = "dst7S8RQUovuUPSMuD"  # 货物明细表
SUPPLIER_TABLE = "dstdGpLM8MeLRDp8dG"  # 供应商表
SUPPLIER_VIEW = "viw8Uu737vJTD"  # 供应商视图

# 全局配置
config = {
    "BASE_URL": os.getenv("MCP_BASE_URL", "https://data.cfcsc.net/fusion/v1"),
    "API_TOKEN": os.getenv("MCP_API_TOKEN", "usksSTtJfU2ysIOd9Z7EF16"),
    "SPACE_ID": os.getenv("MCP_SPACE_ID", "spcjmFHvL3hKh")
}

def init_config(base_url: str, api_token: str, space_id: str):
    """初始化配置"""
    config["BASE_URL"] = base_url
    config["API_TOKEN"] = api_token
    config["SPACE_ID"] = space_id

def get_headers():
    return {
        "Authorization": f"Bearer {config['API_TOKEN']}",
        "Content-Type": "application/json"
    }

def get_pending_dispatch_details(view_id: str = "viwznDHpD5u3T") -> List[dict]:
    """获取待指派的货物明细"""
    url = f"{config['BASE_URL']}/datasheets/{GOODS_DETAIL_TABLE}/records"
    params = {"viewId": view_id}
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            return data['data'].get('records', [])
    return []

def find_records_by_order_numbers(records: List[dict], order_numbers: List[str]) -> List[dict]:
    """从待指派明细中找到指定订单号对应的记录"""
    matched_records = []
    missing_orders = []
    
    # 先检查所有订单号是否都能找到
    for order_number in order_numbers:
        found = False
        for record in records:
            if order_number in record.get('fields', {}).get('订单编号引用', []):
                found = True
                break
        if not found:
            missing_orders.append(order_number)
    
    # 如果有任何订单号找不到，返回空列表
    if missing_orders:
        return []
    
    # 所有订单号都能找到，收集所有匹配的记录
    for record in records:
        order_refs = record.get('fields', {}).get('订单编号引用', [])
        for order_number in order_numbers:
            if order_number in order_refs:
                matched_records.append(record)
                break
    
    return matched_records

def create_external_dispatch(supplier_name: str, dispatch_type: str, record_ids: List[str]) -> Tuple[bool, str]:
    """创建外部派车记录"""
    try:
        # 获取供应商ID
        url = f"{config['BASE_URL']}/datasheets/{SUPPLIER_TABLE}/records"
        params = {
            "viewId": SUPPLIER_VIEW,
            "fieldKey": "name"
        }
        response = requests.get(url, headers=get_headers(), params=params)
        
        if response.status_code != 200:
            return False, "获取供应商ID失败"
            
        data = response.json()
        if not data.get('success'):
            return False, "获取供应商ID失败"
            
        supplier_id = None
        for record in data['data'].get('records', []):
            if record.get('fields', {}).get('供应商名称') == supplier_name:
                supplier_id = record['recordId']
                break
                
        if not supplier_id:
            return False, "未找到匹配的供应商记录"
            
        # 创建派车记录
        dispatch_type_map = {
            "提货": "W提货",
            "送货": "W送货",
            "干线": "W干线"
        }
        
        if dispatch_type not in dispatch_type_map:
            return False, "无效的指派类型"
            
        create_url = f"{config['BASE_URL']}/datasheets/{SUPPLIER_DISPATCH_TABLE}/records"
        create_data = {
            "records": [{
                "fields": {
                    "未派车货物明细": record_ids,
                    "供应商": [supplier_id],
                    "指派类型": [dispatch_type_map[dispatch_type]],
                    "作废标志": "否"
                }
            }]
        }
        
        response = requests.post(create_url, headers=get_headers(), json=create_data)
        return response.status_code == 200 and response.json().get('success', False), ""
        
    except Exception as e:
        return False, str(e)

@mcp.tool(description="批量外部派车，支持多组订单号、供应商和指派类型")
async def batch_external_dispatch(dispatch_groups: List[Dict]) -> Dict:
    """
    批量外部派车函数
    :param dispatch_groups: 派车组列表，每个组为JSON格式：
        {
            "order_numbers": ["订单号1", "订单号2"],
            "supplier_name": "供应商名称",
            "dispatch_type": "指派类型"
        }
    :return: 处理结果，包含成功数量和失败信息
    """
    success_count = 0
    failed_groups = []
    
    try:
        # 获取待指派的货物明细
        records = get_pending_dispatch_details()
        if not records:
            return {
                "success": False,
                "message": "未找到待指派的货物明细",
                "success_count": 0,
                "failed_groups": dispatch_groups
            }
            
        # 处理每组派车信息
        for group in dispatch_groups:
            order_numbers = group["order_numbers"]
            supplier_name = group["supplier_name"]
            dispatch_type = group["dispatch_type"]
            
            # 查找指定订单号的记录
            matched_records = find_records_by_order_numbers(records, order_numbers)
            if not matched_records:
                failed_groups.append({
                    "order_numbers": order_numbers,
                    "reason": "未找到匹配的货物明细记录"
                })
                continue
                
            # 创建外部派车记录
            record_ids = [record['recordId'] for record in matched_records]
            success, error_message = create_external_dispatch(supplier_name, dispatch_type, record_ids)
            if success:
                success_count += 1
            else:
                failed_groups.append({
                    "order_numbers": order_numbers,
                    "reason": error_message
                })
                
        return {
            "success": True,
            "message": "批量派车处理完成",
            "success_count": success_count,
            "failed_groups": failed_groups
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"批量派车过程中发生错误: {str(e)}",
            "success_count": success_count,
            "failed_groups": failed_groups
        }

if __name__ == "__main__":
    # 启动MCP服务
    mcp.run(transport="stdio") 