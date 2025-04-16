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

# 全局配置usksSTtJfU2ysIOd9Z7EF16
config = {
    "BASE_URL": os.getenv("MCP_BASE_URL"),
    "API_TOKEN": os.getenv("MCP_API_TOKEN"),
    "SPACE_ID": os.getenv("MCP_SPACE_ID")
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
    all_records = []
    page_size = 1000  # 每页1000条记录
    page_index = 0
    
    while True:
        url = f"{config['BASE_URL']}/datasheets/{GOODS_DETAIL_TABLE}/records"
        params = {
            "viewId": view_id,
            "pageSize": page_size,
            "pageNum": page_index + 1  # API可能是从1开始计数
        }
        print(f"\n请求第{page_index + 1}页数据:")
        print(f"URL: {url}")
        print(f"参数: {params}")
        
        response = requests.get(url, headers=get_headers(), params=params)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                records = data['data'].get('records', [])
                total = data['data'].get('total', 0)
                print(f"本页获取到 {len(records)} 条记录")
                print(f"总记录数: {total}")
                
                if not records:  # 如果没有更多数据了
                    break
                    
                all_records.extend(records)
                print(f"当前已获取: {len(all_records)}/{total} 条记录")
                
                if len(all_records) >= total:  # 如果已经获取了所有数据
                    break
                    
                page_index += 1
            else:
                print(f"请求失败: {data.get('message', '未知错误')}")
                break
        else:
            print(f"请求失败: HTTP {response.status_code}")
            break
            
    print(f"\n最终获取到 {len(all_records)} 条记录")
    return all_records

def find_records_by_order_numbers(records: List[dict], order_numbers: List[str]) -> Tuple[List[dict], List[str]]:
    """从待指派明细中找到指定订单号对应的记录，并返回相关的派车记录ID
    
    Args:
        records: 待指派明细记录列表
        order_numbers: 订单号列表
        
    Returns:
        Tuple[List[dict], List[str]]: (匹配的货物明细记录列表, 相关的派车记录ID列表)
    """
    matched_records = []
    dispatch_record_ids = []
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
        return [], []
    
    # 所有订单号都能找到，收集所有匹配的记录和派车记录ID
    for record in records:
        order_refs = record.get('fields', {}).get('订单编号引用', [])
        for order_number in order_numbers:
            if order_number in order_refs:
                matched_records.append(record)
                # 获取供应商派车字段的值
                dispatch_ids = record.get('fields', {}).get('供应商派车', [])
                dispatch_record_ids.extend(dispatch_ids)
                break
    
    return matched_records, list(set(dispatch_record_ids))  # 使用set去重

def get_supplier_by_name(supplier_name: str) -> Tuple[bool, str, str]:
    """根据供应商名称查询供应商记录ID
    
    Args:
        supplier_name: 供应商名称
        
    Returns:
        Tuple[bool, str, str]: (是否成功, 供应商ID, 错误信息)
    """
    try:
        url = f"{config['BASE_URL']}/datasheets/{SUPPLIER_TABLE}/records"
        params = {
            "viewId": SUPPLIER_VIEW,
            "filterByFormula": f"供应商名称 = '{supplier_name}'",
            "fieldKey": "name"
        }
        print(f"\n查询供应商ID:")
        print(f"URL: {url}")
        print(f"参数: {params}")
        
        response = requests.get(url, headers=get_headers(), params=params)
        if response.status_code != 200:
            return False, "", f"查询供应商失败: HTTP {response.status_code}"
            
        data = response.json()
        if not data.get('success'):
            return False, "", f"查询供应商失败: {data.get('message', '未知错误')}"
            
        records = data['data'].get('records', [])
        if not records:
            return False, "", f"未找到供应商: {supplier_name}"
            
        return True, records[0]['recordId'], ""
        
    except Exception as e:
        return False, "", f"查询供应商异常: {str(e)}"

def check_dispatch_status(dispatch_record_ids: List[str], supplier_name: str) -> Tuple[bool, str]:
    """检查外部派车记录是否属于指定供应商
    
    Args:
        dispatch_record_ids: 外部派车记录ID列表（从货物明细的供应商派车字段获取）
        supplier_name: 供应商名称
        
    Returns:
        Tuple[bool, str]: (是否已指派给该供应商, 错误信息)
    """
    try:
        # 获取供应商ID
        success, supplier_id, error = get_supplier_by_name(supplier_name)
        if not success:
            return False, error
            
        # 检查每个外部派车记录
        for dispatch_id in dispatch_record_ids:
            success, dispatch_record, error = get_record_by_id(SUPPLIER_DISPATCH_TABLE, dispatch_id)
            if not success:
                print(f"查询派车记录失败: {error}")
                continue
                
            # 检查供应商是否匹配（比较recordId）
            fields = dispatch_record.get('fields', {})
            record_supplier_ids = fields.get('供应商', [])  # 获取供应商ID列表
            if record_supplier_ids and supplier_id in record_supplier_ids:
                return True, f"已存在派车记录，供应商: {supplier_name}"
                
        return False, ""
        
    except Exception as e:
        return False, f"检查派车状态异常: {str(e)}"

def create_external_dispatch(supplier_name: str, dispatch_type: str, detail_record_ids: List[str], dispatch_record_ids: List[str] = None) -> Tuple[bool, str]:
    """创建外部派车记录
    
    Args:
        supplier_name: 供应商名称
        dispatch_type: 指派类型
        detail_record_ids: 货物明细记录ID列表
        dispatch_record_ids: 已有的派车记录ID列表（可选）
    """
    try:
        # 如果有派车记录，检查是否已经指派给该供应商
        if dispatch_record_ids:
            is_dispatched, error_msg = check_dispatch_status(dispatch_record_ids, supplier_name)
            if is_dispatched:
                return False, error_msg
                
        # 获取供应商ID
        success, supplier_id, error = get_supplier_by_name(supplier_name)
        if not success:
            return False, error
            
        # 创建派车记录
        dispatch_type_map = {
            "提货": "W提货",
            "送货": "W送货",
            "干线": "W干线"
        }
        
        if dispatch_type not in dispatch_type_map:
            return False, f"无效的指派类型: {dispatch_type}"
            
        create_url = f"{config['BASE_URL']}/datasheets/{SUPPLIER_DISPATCH_TABLE}/records"
        create_data = {
            "records": [{
                "fields": {
                    "未派车货物明细": detail_record_ids,
                    "供应商": [supplier_id],
                    "指派类型": [dispatch_type_map[dispatch_type]],
                    "作废标志": "否"
                }
            }]
        }
        
        print(f"\n创建派车记录请求:")
        print(f"URL: {create_url}")
        print(f"请求数据: {json.dumps(create_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(create_url, headers=get_headers(), json=create_data)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text[:200]}...")
        
        if response.status_code == 201:
            print("派车记录创建成功！")
            return True, ""
            
        if response.status_code != 200:
            return False, f"创建派车记录失败: HTTP {response.status_code}"
            
        data = response.json()
        if not data.get('success'):
            return False, f"创建派车记录失败: {data.get('message', '未知错误')}"
            
        return True, ""
        
    except Exception as e:
        return False, f"创建派车记录异常: {str(e)}"

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
            matched_records, dispatch_record_ids = find_records_by_order_numbers(records, order_numbers)
            if not matched_records:
                failed_groups.append({
                    "order_numbers": order_numbers,
                    "reason": "未找到匹配的货物明细记录"
                })
                continue
                
            # 创建外部派车记录
            record_ids = [record['recordId'] for record in matched_records]
            success, error_message = create_external_dispatch(supplier_name, dispatch_type, record_ids, dispatch_record_ids)
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

def get_record_by_id(dst_id: str, record_id: str) -> Tuple[bool, dict, str]:
    """根据数据表ID和记录ID查询单条记录
    
    Args:
        dst_id: 数据表ID
        record_id: 记录ID
        
    Returns:
        Tuple[bool, dict, str]: (是否成功, 记录数据, 错误信息)
    """
    try:
        url = f"{config['BASE_URL']}/datasheets/{dst_id}/records"
        params = {
            "recordIds": [record_id],
            "fieldKey": "name"
        }
        print(f"\n查询记录详情:")
        print(f"URL: {url}")
        print(f"参数: {params}")
        
        response = requests.get(url, headers=get_headers(), params=params)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code != 200:
            return False, {}, f"查询记录失败: HTTP {response.status_code}"
            
        data = response.json()
        if not data.get('success'):
            return False, {}, f"查询记录失败: {data.get('message', '未知错误')}"
            
        records = data['data'].get('records', [])
        if not records:
            return False, {}, f"未找到记录ID: {record_id}"
            
        return True, records[0], ""
        
    except Exception as e:
        return False, {}, f"查询记录异常: {str(e)}"

if __name__ == "__main__":
    # 启动MCP服务
    mcp.run(transport="stdio") 