import json
import random
import time
import requests
from smartpush.utils import ListDictUtils


def get_current_flow(host_domain, cookies, flow_id):
    # 提取flow所有节点数据
    _url = host_domain + "/flow/getFlowDetail"
    headers = {
        "cookie": cookies
    }
    params = {
        "flowId": flow_id,
        "active": True,
        "includeActivityDetail": True
    }
    result = json.loads(requests.request(method="get", url=_url, headers=headers, params=params).text)
    # 按节点id存储
    node_counts = []

    def process_node(node):
        node_counts.append({node["id"]: {"completedCount": node["data"]["completedCount"],
                                         "skippedCount": node["data"]["skippedCount"],
                                         "openUserCount": node["data"]["openUserCount"],
                                         "clickUserCount": node["data"]["clickUserCount"],
                                         "waitingCount": node["data"]["waitingCount"]
                                         }
                            }
                           )
        # 处理split节点
        if "split" in node["data"].keys():
            for branch_node in node['data']['split']['branches']["false"]:
                process_node(branch_node)
            for branch_node in node['data']['split']['branches']["true"]:
                process_node(branch_node)
        # 处理abTesting节点
        elif "abTesting" in node["data"].keys():
            for branch_node in node['data']['abTesting']['branches']["a"]:
                process_node(branch_node)
            for branch_node in node['data']['abTesting']['branches']["b"]:
                process_node(branch_node)

    # 处理所有顶层节点
    for node in result['resultData']['nodes']:
        process_node(node)
    return node_counts, result["resultData"]["version"]


def update_flow(host_domain, cookies, **kwargs):
    """
    # 更新flow
    update_flow_params: 必填，saveFlow接口所有参数，dict格式
    version: 非必填，flow版本号
    """
    _url = host_domain + "/flow/saveFlow"
    headers = {
        "cookie": cookies,
        "Content-Type": "application/json"
    }
    kwargs["update_flow_params"]["version"] = kwargs.get("version", kwargs["update_flow_params"]["version"])
    params = kwargs["update_flow_params"]
    result = requests.request(method="post", url=_url, headers=headers, json=params).text


def start_flow(host_domain, cookies, flow_id, version):
    # 开启flow
    _url = host_domain + "/flow/publishFlow"
    headers = {
        "cookie": cookies,
        "Content-Type": "application/json"
    }
    params = {
        "flowId": flow_id,
        "version": str(version)
    }
    result = requests.request(method="post", url=_url, headers=headers, json=params).text


def mock_pulsar(mock_domain, pulsar, limit=1):
    """
    # post请求
    # times：为触发次数，默认1次即可
    """
    _url = mock_domain + "/flow/testEventMulti"
    headers = {
        "Content-Type": "application/json"
    }
    # 生成随机message_id
    prefix = 179
    pulsar["messageId"] = f"{prefix}{random.randint(10 ** 15, 10 ** 16 - 1)}"
    params = {
        "times": limit,
        "mq": pulsar
    }
    result = requests.request(method="post", url=_url, headers=headers, json=params).text
    return json.loads(result)


def check_flow(mock_domain, host_domain, cookies, **kwargs):
    """
    params
    mock_domain:必填，触发接口域名
    host_domain:必填，spflow接口域名
    cookies:必填，sp登录态
    flow_id:必填
    pulsar:必填，模拟的触发数据
    limit:非必填，默认为1 - mock_pulsar函数用于控制模拟触发的次数
    num:非必填，默认为1 - compare_lists函数用于断言方法做差值计算
    update_flow_params: 非必填，dict格式，需更新flow时传参，参数结构为sp的saveFlow接口内容
    """
    # 触发前提取flow数据，后续做对比
    old_flow_counts, old_versions = get_current_flow(host_domain=host_domain, cookies=cookies,
                                                     flow_id=kwargs["flow_id"])
    # 更新flow
    if kwargs.get("update_flow_params", False):
        update_flow(host_domain=host_domain, cookies=cookies, update_flow_params=kwargs.get("update_flow_params"),
                    version=old_versions)
    # 启动flow
    start_flow(host_domain=host_domain, cookies=cookies, flow_id=kwargs["flow_id"], version=old_versions)
    # 触发flow
    mock_pulsar(mock_domain=mock_domain, pulsar=kwargs["pulsar"], limit=kwargs.get("limit", 1))
    # 触发后提取flow数据，做断言
    time.sleep(30)
    new_flow_counts, new_versions = get_current_flow(host_domain=host_domain, cookies=cookies,
                                                     flow_id=kwargs["flow_id"])
    # 断言
    result = ListDictUtils.compare_lists(temp1=old_flow_counts, temp2=new_flow_counts, num=kwargs.get("num", 1))
    return [True, "断言成功"] if len(result) == 0 else [False, result]
