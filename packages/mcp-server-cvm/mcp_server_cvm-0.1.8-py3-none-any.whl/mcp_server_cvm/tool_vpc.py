"""
腾讯云 VPC 相关操作工具模块
"""
import json
from tencentcloud.vpc.v20170312 import models as vpc_models
from .client import get_vpc_client

def describe_security_groups(region: str, security_group_ids: list[str] = None) -> str:
    """查询安全组列表
    
    Args:
        region: 地域，如 ap-guangzhou
        security_group_ids: 安全组ID列表
    """
    client = get_vpc_client(region)
    req = vpc_models.DescribeSecurityGroupsRequest()
    
    params = {}
    if security_group_ids:
        params["SecurityGroupIds"] = security_group_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeSecurityGroups(req)
    return resp.to_json_string()

def describe_vpcs(region: str, vpc_ids: list[str] = None, is_default: bool = None, vpc_name: str = None) -> str:
    """查询VPC列表
    
    Args:
        region: 地域，如 ap-guangzhou
        vpc_ids: VPC ID列表
        is_default: 是否是默认VPC，True表示默认VPC，False表示非默认VPC，None表示不过滤
        vpc_name: VPC名称，用于过滤指定名称的VPC
    
    Returns:
        str: VPC列表的JSON字符串
    """
    client = get_vpc_client(region)
    req = vpc_models.DescribeVpcsRequest()
    
    params = {}
    filters = []
    
    if vpc_ids:
        params["VpcIds"] = vpc_ids
        
    if is_default is not None:
        filters.append({
            "Name": "is-default",
            "Values": ["true" if is_default else "false"]
        })
        
    if vpc_name:
        filters.append({
            "Name": "vpc-name",
            "Values": [vpc_name]
        })
        
    if filters:
        params["Filters"] = filters
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeVpcs(req)
    return resp.to_json_string()

def describe_subnets(region: str, vpc_id: str = None, subnet_ids: list[str] = None, zone: str = None, is_default: bool = None, vpc_name: str = None) -> str:
    """查询子网列表
    
    Args:
        region: 地域，如 ap-guangzhou
        vpc_id: VPC ID，用于过滤指定VPC下的子网
        subnet_ids: 子网ID列表，用于查询指定子网的信息
        zone: 可用区，如 ap-guangzhou-1，用于过滤指定可用区的子网
        is_default: 是否是默认子网，True表示默认子网，False表示非默认子网，None表示不过滤
        vpc_name: VPC名称，用于过滤指定VPC名称下的子网
    
    Returns:
        str: 子网列表的JSON字符串
    """
    client = get_vpc_client(region)
    req = vpc_models.DescribeSubnetsRequest()
    
    params = {}
    filters = []
    
    if vpc_id:
        filters.append({
            "Name": "vpc-id",
            "Values": [vpc_id]
        })
    
    if zone:
        filters.append({
            "Name": "zone",
            "Values": [zone]
        })
        
    if is_default is not None:
        filters.append({
            "Name": "is-default",
            "Values": ["true" if is_default else "false"]
        })
        
    if vpc_name:
        filters.append({
            "Name": "vpc-name",
            "Values": [vpc_name]
        })
        
    if filters:
        params["Filters"] = filters
        
    if subnet_ids:
        params["SubnetIds"] = subnet_ids
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeSubnets(req)
    return resp.to_json_string() 