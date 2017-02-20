# -*- coding: utf-8 -*-

from  aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from  aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from  ParsingPublicIPAddr import getPubIPAddr
from aliyunsdkcore import client
from AccessKeyParser import *
import json

ak_parser = AccessKeyParser()
regionId = 'cn-hangzhou'
domain_name = 'abysswatcher.xyz'


def getCurrentIP(ResList):
    items = []
    for item in ResList["DomainRecords"]["Record"]:
        if item["Status"] == 'ENABLE':
            items.append(item["Value"])

    return items[0]


clt = client.AcsClient(ak_parser.getAccessKeyId(), ak_parser.getAccessKeySecrect(), regionId)
# 构造修改解析记录的请求
update_request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
update_request.set_action_name("UpdateDomainRecord")
update_request.set_Type("A")
update_request.set_RR("abysswatcher.xyz")
update_request.set_Value(getPubIPAddr())
# 发起修改请求，下面会读取解析列表进行验证
clt.do_action(update_request)

# 构造读取解析列表的请求
query_request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
query_request.set_DomainName(domain_name)
query_request.set_accept_format('json')
# 发起请求，获取结果
result = clt.do_action(query_request)
# 将json格式的字典转化为 python 列表格式
json_to_pylist = json.loads(result)


# print json_to_pylist
print getCurrentIP(json_to_pylist)
