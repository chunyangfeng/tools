#!/usr/bin/env python
# coding:utf-8
# Author:Fengchunyang
"""
阿里云ECS和RDS接口调用
"""
import json
from traceback import format_exc
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkrds.request.v20140815 import (
    DescribeDBInstancesRequest, DescribeDBInstanceAttributeRequest, DescribeRegionsRequest, CreateDBInstanceRequest,
    ModifyDBInstanceDescriptionRequest, DescribeAccountsRequest, CreateAccountRequest, ModifySecurityIpsRequest,
    DescribeAvailableResourceRequest, DescribeResourceUsageRequest,DescribeBackupPolicyRequest,ModifyBackupPolicyRequest,
    DescribeBackupTasksRequest,DescribeDBInstanceIPArrayListRequest, DescribeDBInstancePerformanceRequest
)
from aliyunsdkvpc.request.v20160428 import DescribeVpcsRequest, DescribeVSwitchAttributesRequest
from aliyunsdkcms.request.v20190101 import (
    PutContactGroupRequest, DescribeMonitorGroupsRequest, CreateMonitorGroupRequest, ApplyMetricRuleTemplateRequest,
    ModifyMonitorGroupRequest, ModifyMonitorGroupInstancesRequest, CreateMetricRuleTemplateRequest,
    ModifyMetricRuleTemplateRequest, DescribeMetricRuleTemplateListRequest, DescribeEventRuleListRequest,
    DeleteMetricRuleTemplateRequest,DescribeAlertHistoryListRequest, DescribeMetricRuleListRequest

)


class AliyunHandler:
    def __init__(self):
        self.key = "xxx"
        self.secret = "xxx"
        self.region = "cn-beijing"
        self.client = AcsClient(self.key, self.secret, self.region)

    def get_ecs_count(self):
        """获取当前时刻的ECS实例总数"""
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageSize(1)
        response = self.client.do_action_with_exception(request)
        data = json.loads(response.decode())
        return data.get("TotalCount")

    def get_rds_count(self):
        """获取当前时刻的RDS实例总数"""
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_PageSize(1)
        request.set_accept_format("json")
        response = self.client.do_action_with_exception(request)
        data = json.loads(response.decode())
        return data.get("TotalRecordCount")

    def get_rds_instance_by_page(self, pnum, psize=30):
        """
        获取指定页数的指定数量的RDS实例数据
        :param pnum: 页码数
        :param psize: 每页个数
        :return: 实例ID列表
        """
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_PageSize(psize)
        request.set_PageNumber(pnum)
        response = self.client.do_action_with_exception(request)
        data = json.loads(response.decode())
        return [d.get("DBInstanceId") for d in data.get("Items").get("DBInstance")]

    def get_rds_attr_by_id(self, inst_id):
        """
        根据指定的实例ID获取RDS的属性
        :param inst_id: 实例ID列表，最大支持30个
        :return: RDS实例数据列表
        """
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_DBInstanceId(",".join(inst_id))
        response = self.client.do_action_with_exception(request)
        data = json.loads(response.decode())
        return data.get("Items").get("DBInstanceAttribute")

    def get_instance_by_page(self, pnum, psize=30):
        """
        获取指定页数的指定数量的ECS实例数据
        :param pnum: 页码数
        :param psize: 每页个数
        :return: 实例数据
        """
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_PageSize(psize)
        request.set_PageNumber(pnum)
        response = self.client.do_action_with_exception(request)
        data = json.loads(response.decode())
        return data.get("Instances").get("Instance")

    def get_rds_by_id(self, inst_id):
        """
        通过指定ID获取RDS数据
        :param inst_id: 实例ID
        :return: 实例数据是否存在的标记
        """
        flag = True  # 实例是否存在的标记位
        try:
            request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
            request.set_DBInstanceId(inst_id)
            response = self.client.do_action_with_exception(request)
            data = json.loads(response.decode())
            # 处于释放状态的实例依然能查询，但是不会返回数据也不会触发异常，需要单独处理
            if data.get("TotalRecordCount") == 0:
                flag = False
        except ServerException:
            print("ID为 {0} 的RDS实例不存在".format(inst_id))
            flag = False
        return flag

    def get_region(self):
        """
        获取可用区数据
        :return:
        """
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format("json")
        response = self.client.do_action_with_exception(request)
        print(response)

    def get_vpc(self):
        """
        获取全部VPC网络信息
        :return: [{vpc_id:'', cidr: '', vpc_name: ''}]
        """
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        data = []
        for d in json.loads(response).get("Vpcs").get('Vpc'):
            data.append({
                'cidr': d.get('CidrBlock'),
                'vpc_id': d.get('VpcId'),
                'vpc_name': d.get('VpcName'),
            })
        return data

    def get_vsw_by_vpcid(self, vpcid):
        """
        通过VPCID获取其下所有交换机的VSWID
        :param vpcid: VPCID
        :return: 由VSWID组成的列表
        """
        request = DescribeVpcsRequest.DescribeVpcsRequest()
        request.set_accept_format('json')
        request.set_VpcId(vpcid)
        response = self.client.do_action_with_exception(request)
        data = json.loads(response.decode())
        return data.get("Vpcs").get("Vpc")[0].get("VSwitchIds").get("VSwitchId")

    def get_vsw_by_vswid(self, vswid):
        """
        通过VSWID获取vsw属性描述
        :param vswid: VSWID
        :return: vsw的详细属性字典
        """
        request = DescribeVSwitchAttributesRequest.DescribeVSwitchAttributesRequest()
        request.set_accept_format('json')
        request.set_VSwitchId(vswid)
        response = self.client.do_action_with_exception(request)
        return json.loads(response.decode())

    def create_rds(self, order):
        """
        创建RDS，详情见https://help.aliyun.com/document_detail/26228.html?spm=a2c4g.11174283.6.1496.d75b4c22YL3TQ7
        :return:
        """
        request = CreateDBInstanceRequest.CreateDBInstanceRequest()
        request.set_accept_format("json")
        request.set_ClientToken(order.token)
        request.set_Engine(order.engine)
        request.set_EngineVersion(order.version)
        request.set_DBInstanceClass(order.spec)
        request.set_DBInstanceStorage(order.storage)
        request.set_DBInstanceNetType("Intranet")
        request.set_PayType(order.pay_type)
        request.set_DBInstanceDescription("{0}-{1}-{2}-{3}-正常".format(order.env, order.business, order.sdm, order.center))
        request.set_ZoneId(order.zone)
        request.set_InstanceNetworkType("VPC")
        request.set_VPCId(order.vpc)
        request.set_VSwitchId(order.vsw)
        int_duration = int(order.duration)
        if order.pay_type == "Prepaid":
            if int_duration <= 11:
                period = "Month"
                used_time = int_duration
            else:
                period = "Year"
                used_time = int_duration // 12
            request.set_Period(period)  # 包年还是包月
            request.set_UsedTime(used_time)  # 时长
            request.set_AutoRenew(True if order.auto_renew == 'true' else False)  # 自动续费
        request.set_DBInstanceStorageType(order.storage_type)
        if order.white_list:
            request.set_SecurityIPList(order.white_list + ',127.0.0.1')  # 白名单
        else:
            request.set_SecurityIPList('127.0.0.1')  # 白名单
        request.set_Category(order.category)
        request.set_read_timeout(60)
        data = {}

        try:
            response = self.client.do_action_with_exception(request)
            data = json.loads(response.decode())
        except Exception as error:
            print(error)
        return data

    def modify_rds_desc(self, inst_id, desc):
        """
        修改制定RDS实例的名称（即描述）
        :param inst_id: RDS实例ID
        :param desc: 名称信息
        :return:
        """
        request = ModifyDBInstanceDescriptionRequest.ModifyDBInstanceDescriptionRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(inst_id)
        request.set_DBInstanceDescription(desc)
        response = self.client.do_action_with_exception(request)
        print("RDS实例：{0}的名称已修改为 {1}".format(inst_id, desc))
        return

    def get_account(self, inst_id):
        """
        获取指定RDS实例的账号信息
        :param inst_id: 实例ID
        :return:
        """
        request = DescribeAccountsRequest.DescribeAccountsRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(inst_id)
        response = self.client.do_action_with_exception(request)
        account = []
        for acc in json.loads(response).get("Accounts").get('DBInstanceAccount'):
            account.append(acc.get("AccountName"))
        return list(set(account))

    def create_account(self, inst_id, account, password):
        """
        给指定的RDS实例创建账号
        :param inst_id: 实例ID
        :param account: 用户名
        :param password: 密码
        :return:
        """
        accounts = self.get_account(inst_id)
        if account in accounts:
            response = "{0}账号已存在，创建账号任务取消".format(inst_id)
        else:
            request = CreateAccountRequest.CreateAccountRequest()
            request.set_accept_format('json')
            request.set_DBInstanceId(inst_id)
            request.set_AccountName(account)
            request.set_AccountPassword(password)
            response = self.client.do_action_with_exception(request)
        return response

    def get_white_list(self, inst_id):
        """
        获取指定实例的白名单列表
        :param inst_id: RDS实例ID
        :return: 白名单IP列表
        """
        request = DescribeDBInstanceIPArrayListRequest.DescribeDBInstanceIPArrayListRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(inst_id)
        response = self.client.do_action_with_exception(request)
        data = []
        for wi in json.loads(response).get('Items').get('DBInstanceIPArray'):
            for ip in wi.get('SecurityIPList').split(','):
                data.append(ip)
        return list(set(data))

    def set_white_list(self, inst_id, ips, group='baoleiji'):
        """
        将指定的IP地址加入指定的RDS实例的白名单中
        :param inst_id: RDS实例ID（string）
        :param ips: ip地址，多个ip以英文逗号隔开（string）
        :param group: 要操作的白名单分组名称，默认baoleiji分组
        :return:
        """
        request = ModifySecurityIpsRequest.ModifySecurityIpsRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(inst_id)
        request.set_SecurityIps(ips)
        request.set_DBInstanceIPArrayName(group)  # 指定要操作的白名单分组
        request.set_ModifyMode('Append')
        response = self.client.do_action_with_exception(request)
        return response

    def modify_contact_group(self, users, desc, group_name="DBA_值班"):
        """
        修改报警联系人组的联系人信息
        :param users:  被添加进报警组的用户名(type:list)
        :param desc:  报警组描述
        :param group_name:  被操作的报警组名
        :return:
        """
        request = PutContactGroupRequest.PutContactGroupRequest()
        request.set_accept_format("json")
        request.set_ContactGroupName(group_name)
        request.set_ContactNamess(users)
        request.set_Describe(desc)
        response = self.client.do_action_with_exception(request)
        return response

    def get_available_resource(self, pay_type, zone_id=None, engine=None, engine_version=None, spec=None, storage_type=None):
        """
        获取指定参数下的可用资源，https://help.aliyun.com/document_detail/134039.html
        :param pay_type: 付费类型
        :param zone_id: 可用区ID
        :param engine: 数据库类型
        :param engine_version: 数据库版本
        :param spec: 实例规格
        :param storage_type: 存储类型
        :return:
        """
        request = DescribeAvailableResourceRequest.DescribeAvailableResourceRequest()
        request.set_accept_format("json")
        request.set_InstanceChargeType(pay_type)
        request.set_read_timeout(60)
        if zone_id:
            request.set_ZoneId(zone_id)
        if engine:
            request.set_Engine(engine)
        if engine_version:
            request.set_EngineVersion(engine_version)
        if spec:
            request.set_DBInstanceClass(spec)
        if storage_type:
            request.set_DBInstanceStorageType(storage_type)
        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def get_resource_usage(self, inst_id):
        """
        获取RDS实例的资源使用情况
        :param inst_id: 实例ID
        :return:
        """
        request = DescribeResourceUsageRequest.DescribeResourceUsageRequest()
        request.set_accept_format("json")
        request.set_DBInstanceId(inst_id)
        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def get_monitor_group(self, name=None, inst_id=None):
        """
        查询指定名称的应用分组是否存在
        :param name: 应用分组名称
        :param inst_id: 应用分组下的实例ID
        :return: group_id
        """
        request = DescribeMonitorGroupsRequest.DescribeMonitorGroupsRequest()
        request.set_accept_format("json")
        if name:
            request.set_GroupName(name)
        if inst_id:
            request.set_InstanceId(inst_id)
        response = self.client.do_action_with_exception(request)
        group_id = []
        if json.loads(response).get('Total'):
            for group in json.loads(response).get("Resources").get('Resource'):
                group_id.append(group.get('GroupId'))
        return group_id

    def create_monitor_group(self, name, contact_group):
        """
        创建应用分组
        :param name: 分组名称
        :param contact_group: 分组报警联系人组
        :return:  创建成功的组ID
        """
        request = CreateMonitorGroupRequest.CreateMonitorGroupRequest()
        request.set_accept_format("json")
        request.set_GroupName(name)
        request.set_ContactGroups(contact_group)
        response = self.client.do_action_with_exception(request)
        return json.loads(response).get('GroupId')

    def bind_tpl_monitor(self, group_id, tpl_id):
        """
        绑定报警模板到应用分组
        :param group_id: 应用分组ID
        :param tpl_id: 报警模板ID
        :return:
        """
        request = ApplyMetricRuleTemplateRequest.ApplyMetricRuleTemplateRequest()
        request.set_accept_format("json")
        request.set_GroupId(group_id)
        request.set_TemplateIds(tpl_id)
        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def modify_monitor_group(self, group_id, contact_group=None, name=None):
        """
        修改应用分组属性
        :param group_id: 应用分组ID
        :param contact_group: 报警联系人组
        :param name: 应用分组名称
        :return:
        """
        request = ModifyMonitorGroupRequest.ModifyMonitorGroupRequest()
        request.set_accept_format("json")
        request.set_GroupId(group_id)
        if contact_group:
            request.set_ContactGroups(contact_group)
        if name:
            request.set_GroupName(name)
        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def modify_monitor_group_instance(self, group_id, inst_id, inst_name, category='RDS', region_id='cn-beijing'):
        """
        修改应用分组中的实例
        :param group_id: 应用分组ID
        :param inst_id: 实例ID
        :param inst_name: 实例名称
        :param category: 实例类型
        :param region_id: 区域ID
        :return:
        """
        request = ModifyMonitorGroupInstancesRequest.ModifyMonitorGroupInstancesRequest()
        request.set_accept_format("json")
        request.set_GroupId(group_id)
        request.set_Instancess([{
            "Category": category,
            'InstanceId': inst_id,
            'RegionId': region_id,
            "InstanceName": inst_name
        }])
        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def create_alert_template(self, name, data):
        """
        创建报警模板（https://help.aliyun.com/document_detail/114984.html）
        :param name:  报警模板名称
        :param data: 报警模板详细数据，具体数据格式参考API文档
        :return: 报警模板ID
        """
        request = CreateMetricRuleTemplateRequest.CreateMetricRuleTemplateRequest()
        request.set_accept_format('json')
        request.set_Name(name)
        request.set_AlertTemplatess(data)
        response = self.client.do_action_with_exception(request)
        return json.loads(response).get("Id")

    def modify_alert_template(self, tpl_id, name=None, desc=None, data=None):
        """
        动态修改RDS报警模板
        :param tpl_id: 报警模板ID
        :param name: 报警模板名称
        :param desc: 报警模板描述
        :param data: 报警模板报警规则数据，参考https://help.aliyun.com/document_detail/114981.html
        :return:
        """
        request = ModifyMetricRuleTemplateRequest.ModifyMetricRuleTemplateRequest()
        request.set_accept_format('json')
        request.set_TemplateId(tpl_id)
        request.set_RestVersion(self.get_alert_template_attr(tpl_id=tpl_id).get('RestVersion'))
        if name:
            request.set_Name(name)
        if desc:
            request.set_Description(desc)
        if data:
            request.set_AlertTemplatess(data)
        response = self.client.do_action_with_exception(request)
        print(response)

    def get_alert_template(self, name=None, tpl_id=None):
        """
        根据指定的报警模板名称或报警模板ID获取报警模板基础信息
        :param name: 报警模板名称
        :param tpl_id: 报警模板ID
        :return: 模板ID列表
        """
        request = DescribeMetricRuleTemplateListRequest.DescribeMetricRuleTemplateListRequest()
        request.set_accept_format('json')
        if name:
            request.set_Name(name)
        if tpl_id:
            request.set_TemplateId(tpl_id)
        response = self.client.do_action_with_exception(request)
        tpl_id = []
        if json.loads(response).get("Total") == 1:
            for tpl in json.loads(response).get('Templates').get('Template'):
                tpl_id.append(tpl.get('TemplateId'))
        return tpl_id

    def get_alert_template_attr(self, name=None, tpl_id=None):
        """
        根据指定的报警模板名称或报警模板ID获取报警模板基础属性数据
        :param name: 报警模板名称
        :param tpl_id: 报警模板ID
        :return: 属性字典
        """
        request = DescribeMetricRuleTemplateListRequest.DescribeMetricRuleTemplateListRequest()
        request.set_accept_format('json')
        if name:
            request.set_Name(name)
        if tpl_id:
            request.set_TemplateId(tpl_id)
        response = self.client.do_action_with_exception(request)
        return json.loads(response).get('Templates').get('Template')[0] if json.loads(response).get('Total') == 1 else {}

    def get_alert_state(self, group_id, prefix=None):
        """
        查询指定应用分组的报警规则启停状态
        :param group_id: 应用分组ID
        :param prefix: 报警规则名前缀，支持模糊搜索
        :return: 启停状态列表
        """
        request = DescribeEventRuleListRequest.DescribeEventRuleListRequest()
        request.set_accept_format('json')
        request.set_GroupId(group_id)
        if prefix:
            request.set_NamePrefix(prefix)
        response = self.client.do_action_with_exception(request)
        status = []
        if json.loads(response).get("Total") > 0:
            for d in json.loads(response).get('EventRules').get('EventRule'):
                status.append(False if d.get('State') == 'DISABLED' else True)
        return status

    def get_backup_policy(self, inst_id):
        """获取备份设置"""
        request = DescribeBackupPolicyRequest.DescribeBackupPolicyRequest()
        request.set_DBInstanceId(inst_id)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def modify_backup_policy(self, inst_id):
        """修改制定实例的备份策略"""
        request = ModifyBackupPolicyRequest.ModifyBackupPolicyRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(inst_id)       # 实例id
        request.set_BackupPolicyMode('DataBackupPolicy')    # 备份模式
        request.set_PreferredBackupTime('17:00Z-18:00Z')    # 备份时间
        request.set_PreferredBackupPeriod('Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday')   # 备份周期
        request.set_BackupRetentionPeriod('30')             # 备份保留天数
        res = self.client.do_action_with_exception(request)
        return json.loads(res)

    def describe_backup_task(self, inst_id):
        """查看备份完成情况"""
        request = DescribeBackupTasksRequest.DescribeBackupTasksRequest()
        request.set_DBInstanceId(inst_id)
        request.set_accept_format('json')
        res = self.client.do_action_with_exception(request)
        return json.loads(res)

    def get_alert_history(self, groupid):
        request = DescribeAlertHistoryListRequest.DescribeAlertHistoryListRequest()
        request.set_accept_format('json')
        request.set_GroupId(groupid)
        res = self.client.do_action_with_exception(request)
        return json.loads(res)

    def get_metric_rulelist(self, groupid, rulename):
        request = DescribeMetricRuleListRequest.DescribeMetricRuleListRequest()
        request.set_accept_format('json')
        request.set_GroupId(groupid)
        request.set_RuleName(rulename)
        res = self.client.do_action_with_exception(request)
        return json.loads(res)

    def get_performance(self, inst_id, keys, stime, etime):
        """
        查询指定指标和时间范围内的RDS指标数据
        :param inst_id: RDS实例ID
        :param keys: 性能指标（type：list），详情见https://help.aliyun.com/document_detail/26316.html?spm=a2c4g.11186623.2.15.37f71575FEfvJe
        :param stime: 开始时间（eg：2020-05-08T15:00Z）
        :param etime: 结束时间（eg：2020-05-08T15:00Z）
        :return:
        """
        request = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(inst_id)
        request.set_Key(",".join(keys))
        request.set_StartTime(stime)
        request.set_EndTime(etime)
        response = self.client.do_action_with_exception(request)
        return json.loads(response).get("PerformanceKeys").get("PerformanceKey")






