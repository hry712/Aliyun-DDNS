# -*- coding: utf-8 -*-

from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkcore import client
from AccessKeyParser import *
import time
import uuid
import urllib
import hmac
from hashlib import sha1
import base64
import httplib
import json


ak_path = "./AccessKeyHolder/test_access_key.csv"

request_params = {
    "Action":"DescribeDomainRecords",
    "DomainName":"abysswatcher.xyz",
    "PageNumber":1,
    "PageSize":20,
    "RRKeyWord":"",
    "TypeKeyWord":"",
    "ValueKeyWord":""
}

common_params = {
    "Format":"json",
    "Version":"2015-01-09",
    "AccessKeyId":"",
    "SignatureMethod":"HMAC-SHA1",
    "SignatureVersion":"1.0",
    "SignatureNonce":"",
    "Timestamp":""
}

common_signature_params = {
    "Signature":None
}

api_serv_addr = "alidns.aliyuncs.com"

def PercentEncode(Str):
    raw_str = str(Str)
    # 这个 quote 方法可令 & = / 这些符号也转变成 % 号的形式
    # 如果没有的话，那么二次转换 can_query_str 的结果会看到没有任何变化
    # 连 / 符号都不能转化
    encoded_str = urllib.quote(raw_str.encode("utf-8"), '')
    replaced_str = encoded_str.replace('+', '%20')\
                            .replace('*', '%2A')\
                            .replace('%7E', '~')
    return replaced_str


def getCanonicalQueryString(RawSortedParams):
    canonical_query_str = ""
    for (key, value) in RawSortedParams:
        canonical_query_str += '&' + PercentEncode(key) +\
            '=' + PercentEncode(value)
    return canonical_query_str

def GenPostRequestHeader():
    return {
        "Content-type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
        "Connection": "Keep-Alive"
    }

def test():
    ak_parser = AccessKeyParser(ak_path)
    common_params["AccessKeyId"] = ak_parser.getAccessKeyId()
    common_params["SignatureNonce"] = str(uuid.uuid1())
    common_params["Timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    intermediate_params = {}
    intermediate_params.update(common_params)
    intermediate_params.update(request_params)
    # print intermediate_params
    # 经典的字典排序用法
    # 由于字典是无序的组合，那么返回形式必将会以有序呈现
    # 返回结果是 [(aa, AA), (bb, BB), ..., (key, value)]
    sorted_params = sorted(intermediate_params.items(), key=lambda intermediate_params: intermediate_params[0])
    can_query_str = getCanonicalQueryString(sorted_params)
    # print can_query_str
    # print
    # print PercentEncode(can_query_str)
    # print
    # print PercentEncode('/')
    str_to_sign = 'POST'+'&'+PercentEncode('/')+'&'+PercentEncode(can_query_str[1:])
    print str_to_sign
    HMAC_key = ak_parser.getAccessKeySecrect()+'&'
    signature_str = base64.b64encode(hmac.new(HMAC_key, str_to_sign, sha1).digest())
    common_signature_params["Signature"] = signature_str
    common_params.update(common_signature_params)

    # 使用 POST 方法时，要把请求参数放到 head 部分
    # 使用 GET 方法时，要把请求参数放到 URL 中
    request_params.update(common_params)
    request_url = "/?" + urllib.urlencode(request_params)
    http_connect = httplib.HTTPConnection(api_serv_addr, 80, timeout=30)
    # print signature_str
    request_head = GenPostRequestHeader()
    http_connect.connect()
    http_connect.request("POST", request_url, None, request_head)
    http_response = http_connect.getresponse()
    result = http_response.read()
    json_py_record = json.loads(result)
    print result
    # 经测试发现，前后两次调用产生的 ReordId 是一样的，这不受调用时间影响
    print json_py_record["DomainRecords"]["Record"][1]["RecordId"]
    http_connect.close()

    clt = client.AcsClient(ak_parser.getAccessKeyId(),
                           ak_parser.getAccessKeySecrect(),
                           'cn-hangzhou')
    request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName('abysswatcher.xyz')
    result = clt.do_action(request)
    print
    print json.loads(result)



if __name__ == '__main__':
    test()
