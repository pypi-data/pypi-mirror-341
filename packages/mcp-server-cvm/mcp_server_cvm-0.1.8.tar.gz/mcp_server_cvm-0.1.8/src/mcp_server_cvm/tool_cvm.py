"""
腾讯云 CVM 相关操作工具模块
"""
import json
from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models
from .client import get_cvm_client
from asyncio.log import logger
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

def describe_regions() -> str:
    """查询地域列表"""
    client = get_cvm_client("ap-guangzhou")  # 使用默认地域
    req = cvm_models.DescribeRegionsRequest()
    resp = client.DescribeRegions(req)
    return resp.to_json_string()

def describe_zones(region: str) -> str:
    """查询可用区列表"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeZonesRequest()
    resp = client.DescribeZones(req)
    return resp.to_json_string()

def describe_instances(region: str, offset: int, limit: int, instance_ids: list[str]) -> str:
    """查询实例列表"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeInstancesRequest()
    
    params = {
        "Offset": offset,
        "Limit": limit
    }
    if instance_ids:
        params["InstanceIds"] = instance_ids
        
    req.from_json_string(json.dumps(params))
    resp = client.DescribeInstances(req)
    
    # 解析返回结果并添加 LoginUrl
    result = json.loads(resp.to_json_string())
    if "Response" in result and "InstanceSet" in result["Response"]:
        for instance in result["Response"]["InstanceSet"]:
            instance_id = instance.get("InstanceId")
            if instance_id:
                instance["LoginUrl"] = f"https://orcaterm.cloud.tencent.com/terminal?type=cvm&instanceId={instance_id}&region={region}"
    
    return json.dumps(result)

def describe_images(region: str, image_ids: list[str] = None, image_type: str = None,
                  platform: str = None, image_name: str = None,
                  offset: int = None, limit: int = None) -> str:
    """查询镜像列表
    
    Args:
        region (str): 地域ID
        image_ids (list[str], optional): 镜像ID列表
        image_type (str, optional): 镜像类型
        platform (str, optional): 操作系统平台
        image_name (str, optional): 镜像名称
        offset (int, optional): 偏移量
        limit (int, optional): 返回数量
        
    Returns:
        str: API响应结果的JSON字符串
    """
    client = get_cvm_client(region)
    req = cvm_models.DescribeImagesRequest()
    
    # 构建参数
    params = {}
    filters = []
    
    # 添加过滤条件
    if image_type:
        filters.append({
            "Name": "image-type",
            "Values": [image_type]
        })
    if platform:
        filters.append({
            "Name": "platform",
            "Values": [platform]
        })
    if image_name:
        filters.append({
            "Name": "image-name",
            "Values": [image_name]
        })
        
    if filters:
        params["Filters"] = filters
    if image_ids:
        params["ImageIds"] = image_ids
    if offset is not None:
        params["Offset"] = offset
    if limit is not None:
        params["Limit"] = limit
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeImages(req)
    return resp.to_json_string()

def describe_instance_type_configs(region: str, zone: str = None, instance_family: str = None) -> str:
    """查询实例机型配置"""
    client = get_cvm_client(region)
    req = cvm_models.DescribeInstanceTypeConfigsRequest()
    
    params = {}
    if zone:
        params["Filters"] = [{
            "Name": "zone",
            "Values": [zone]
        }]
    if instance_family:
        if "Filters" not in params:
            params["Filters"] = []
        params["Filters"].append({
            "Name": "instance-family",
            "Values": [instance_family]
        })
        
    if params:
        req.from_json_string(json.dumps(params))
    resp = client.DescribeInstanceTypeConfigs(req)
    return resp.to_json_string()

def reboot_instances(region: str, instance_ids: list[str], stop_type: str) -> str:
    """重启实例"""
    client = get_cvm_client(region)
    req = cvm_models.RebootInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "StopType": stop_type
    }
    req.from_json_string(json.dumps(params))
    resp = client.RebootInstances(req)
    return resp.to_json_string()

def start_instances(region: str, instance_ids: list[str]) -> str:
    """启动实例"""
    client = get_cvm_client(region)
    req = cvm_models.StartInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids
    }
    req.from_json_string(json.dumps(params))
    resp = client.StartInstances(req)
    return resp.to_json_string()

def stop_instances(region: str, instance_ids: list[str], stop_type: str, stopped_mode: str) -> str:
    """关闭实例"""
    client = get_cvm_client(region)
    req = cvm_models.StopInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "StopType": stop_type,
        "StoppedMode": stopped_mode
    }
    req.from_json_string(json.dumps(params))
    resp = client.StopInstances(req)
    return resp.to_json_string()

def terminate_instances(region: str, instance_ids: list[str]) -> str:
    """销毁实例"""
    client = get_cvm_client(region)
    req = cvm_models.TerminateInstancesRequest()
    
    params = {
        "InstanceIds": instance_ids
    }
    req.from_json_string(json.dumps(params))
    resp = client.TerminateInstances(req)
    return resp.to_json_string()

def reset_instances_password(region: str, instance_ids: list[str], password: str, force_stop: bool) -> str:
    """重置实例密码"""
    client = get_cvm_client(region)
    req = cvm_models.ResetInstancesPasswordRequest()
    
    params = {
        "InstanceIds": instance_ids,
        "Password": password,
        "ForceStop": force_stop
    }
    req.from_json_string(json.dumps(params))
    resp = client.ResetInstancesPassword(req)
    return resp.to_json_string()

def run_instances(region: str, params: dict) -> str:
    """创建实例"""
    try:
        from .run_instances import run_instances as run_instances_impl
        return run_instances_impl(
            region=region,
            zone=params.get("Zone"),
            instance_type=params.get("InstanceType"),
            image_id=params.get("ImageId"),
            vpc_id=params.get("VpcId"),
            subnet_id=params.get("SubnetId"),
            security_group_ids=params.get("SecurityGroupIds"),
            password=params.get("Password"),
            instance_name=params.get("InstanceName"),
            instance_charge_type=params.get("InstanceChargeType"),
            instance_count=params.get("InstanceCount"),
            dry_run=params.get("DryRun", False)
        )
    except Exception as e:
        logger.error(f"创建实例失败: {str(e)}")
        raise e

def reset_instance(region: str, instance_id: str, image_id: str, password: str = None) -> str:
    """重装实例操作系统
    
    Args:
        region (str): 实例所在地域
        instance_id (str): 实例ID
        image_id (str): 重装使用的镜像ID
        password (str, optional): 实例重装后的密码。如果不指定，保持原密码不变
        
    Returns:
        str: API响应结果的JSON字符串
        
    Raises:
        Exception: 当API调用失败时抛出异常
    """
    try:
        client = get_cvm_client(region)
        # 设置实例登录配置
        login_settings = cvm_models.LoginSettings()
        if password:
            login_settings.Password = password
        
        req = cvm_models.ResetInstanceRequest()
        req.InstanceId = instance_id
        req.ImageId = image_id
        req.LoginSettings = login_settings
        resp = client.ResetInstance(req)
        return resp.to_json_string()
    except Exception as e:
        logger.error(f"重装实例操作系统失败: {str(e)}")
        raise e

def inquiry_price_run_instances(region: str, params: dict) -> str:
    """创建实例询价
    
    Args:
        region (str): 实例所在地域
        params (dict): 询价参数，包含：
            - Zone: 可用区
            - InstanceType: 实例机型
            - ImageId: 镜像ID
            - SystemDisk: 系统盘配置
            - InstanceChargeType: 实例计费类型
            - InstanceChargePrepaid: 预付费配置（仅当 InstanceChargeType 为 PREPAID 时需要）
            
    Returns:
        str: API响应结果的JSON字符串
        
    Raises:
        Exception: 当API调用失败时抛出异常
    """
    try:
        client = get_cvm_client(region)
        req = cvm_models.InquiryPriceRunInstancesRequest()
        
        # 设置基础配置
        req.Placement = cvm_models.Placement()
        req.Placement.Zone = params.get("Zone")
        
        req.InstanceType = params.get("InstanceType")
        req.ImageId = params.get("ImageId")
        
        # 设置系统盘
        system_disk = params.get("SystemDisk", {})
        if system_disk:
            req.SystemDisk = cvm_models.SystemDisk()
            req.SystemDisk.DiskType = system_disk.get("DiskType", "CLOUD_PREMIUM")
            req.SystemDisk.DiskSize = system_disk.get("DiskSize", 50)
            
        # 设置计费类型
        req.InstanceChargeType = params.get("InstanceChargeType", "POSTPAID_BY_HOUR")
        
        # 如果是包年包月，设置购买时长
        if req.InstanceChargeType == "PREPAID":
            prepaid = params.get("InstanceChargePrepaid", {})
            req.InstanceChargePrepaid = cvm_models.InstanceChargePrepaid()
            req.InstanceChargePrepaid.Period = prepaid.get("Period", 1)
            req.InstanceChargePrepaid.RenewFlag = prepaid.get("RenewFlag", "NOTIFY_AND_MANUAL_RENEW")
            
        resp = client.InquiryPriceRunInstances(req)
        return resp.to_json_string()
    except Exception as e:
        logger.error(f"创建实例询价失败: {str(e)}")
        raise e

def create_diagnostic_reports(region: str, instance_ids: list[str]) -> str:
    """创建实例诊断报告
    
    Args:
        region: 地域
        instance_ids: 实例ID列表
        
    Returns:
        str: API响应结果的JSON字符串
    """
    try:
        client = get_cvm_client(region)
        params = {
            "InstanceIds": instance_ids
        }
        # 使用通用请求方式调用
        resp = client.call("CreateDiagnosticReports", params)
        # 如果响应是字节类型，先解码成字符串
        if isinstance(resp, bytes):
            resp = resp.decode('utf-8')
        return resp
    except Exception as e:
        logger.error(f"创建实例诊断报告失败: {str(e)}")
        raise e

def describe_diagnostic_reports(region: str, report_ids: list[str] = None,
                              filters: list[dict] = None, vague_instance_name: str = None,
                              offset: int = None, limit: int = None,
                              cluster_diagnostic_report_ids: list[str] = None,
                              scenario_id: int = None) -> str:
    """查询实例诊断报告
    
    Args:
        region: 地域
        report_ids: 实例健康检测报告ID列表，如：["dr-rfmme2si"]。每次请求批量报告ID的上限为100
        filters: 过滤条件列表，支持的过滤条件：
            - instance-id: 按实例ID过滤，如：ins-8jqq9ajy
            - instance-name: 按实例名称过滤，如：my-ins
            - instance-health-status: 按实例健康状态过滤，可选值：Normal, Warn, Critical
            - report-status: 按报告状态过滤，可选值：Querying, Finished
            - cluster-ids: 按集群ID过滤，如：['hpc-rltlmf6v']
        vague_instance_name: 模糊实例别名
        offset: 偏移量，默认为0
        limit: 返回数量，默认为20，最大值为100
        cluster_diagnostic_report_ids: 集群健康检测报告ID列表，如：["cr-rfmme2si"]
        scenario_id: 检测场景ID，默认为1表示对CVM进行全面体检，200为集群一致性检测场景
        
    Returns:
        str: API响应结果的JSON字符串
        
    Note:
        report_ids 和 cluster_diagnostic_report_ids 不能与 filters 或 vague_instance_name 联合使用
    """
    try:
        client = get_cvm_client(region)
        params = {}
        
        if report_ids:
            params["ReportIds"] = report_ids
        if filters:
            params["Filters"] = filters
        if vague_instance_name:
            params["VagueInstanceName"] = vague_instance_name
        if offset is not None:
            params["Offset"] = offset
        if limit is not None:
            params["Limit"] = limit
        if cluster_diagnostic_report_ids:
            params["ClusterDiagnosticReportIds"] = cluster_diagnostic_report_ids
        if scenario_id is not None:
            params["ScenarioId"] = scenario_id
            
        # 使用通用请求方式调用
        resp = client.call("DescribeDiagnosticReports", params)
        # 如果响应是字节类型，先解码成字符串
        if isinstance(resp, bytes):
            resp = resp.decode('utf-8')
        return resp
    except Exception as e:
        logger.error(f"查询实例诊断报告失败: {str(e)}")
        raise e 