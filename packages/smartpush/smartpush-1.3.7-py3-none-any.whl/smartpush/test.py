# -*- codeing = utf-8 -*-
# @Time :2025/2/20 00:27
# @Author :luzebin
import pandas as pd

from smartpush.export.basic import ExcelExportChecker
from smartpush.export.basic.ReadExcel import read_excel_from_oss
from smartpush.export.basic.ReadExcel import read_excel_and_write_to_dict
from smartpush.export.basic.GetOssUrl import get_oss_address_with_retry
from smartpush.utils.DataTypeUtils import DataTypeUtils
from smartpush.flow import MockFlow

if __name__ == '__main__':
    oss1 = "https://cdn.smartpushedm.com/material_ec2/2025-02-26/31c1a577af244c65ab9f9a984c64f3d9/ab%E5%BC%B9%E7%AA%97%E6%B5%8B%E8%AF%952.10%E5%88%9B%E5%BB%BA-%E6%9C%89%E5%85%A8%E9%83%A8%E6%95%B0%E6%8D%AE%E9%94%80%E5%94%AE%E9%A2%9D%E6%98%8E%E7%BB%86%E6%95%B0%E6%8D%AE.xlsx"
    oss2 = "https://cdn.smartpushedm.com/material_ec2/2025-02-26/31c1a577af244c65ab9f9a984c64f3d9/ab%E5%BC%B9%E7%AA%97%E6%B5%8B%E8%AF%952.10%E5%88%9B%E5%BB%BA-%E6%9C%89%E5%85%A8%E9%83%A8%E6%95%B0%E6%8D%AE%E9%94%80%E5%94%AE%E9%A2%9D%E6%98%8E%E7%BB%86%E6%95%B0%E6%8D%AE.xlsx"
    # # print(check_excel_all(oss1, oss1))
    oss3 = "https://cdn.smartpushedm.com/material_ec2/2025-03-07/dca03e35cb074ac2a46935c85de9f510/导出全部客户.csv"
    oss4 = "https://cdn.smartpushedm.com/material_ec2/2025-03-07/c5fa0cc24d05416e93579266910fbd3e/%E5%AF%BC%E5%87%BA%E5%85%A8%E9%83%A8%E5%AE%A2%E6%88%B7.csv"
    expected_oss = "https://cdn.smartpushedm.com/material_ec2/2025-02-26/757df7e77ce544e193257c0da35a4983/%E3%80%90%E8%87%AA%E5%8A%A8%E5%8C%96%E5%AF%BC%E5%87%BA%E3%80%91%E8%90%A5%E9%94%80%E6%B4%BB%E5%8A%A8%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx"
    # actual_oss = "https://cdn.smartpushedm.com/material_ec2/2025-02-26/757df7e77ce544e193257c0da35a4983/%E3%80%90%E8%87%AA%E5%8A%A8%E5%8C%96%E5%AF%BC%E5%87%BA%E3%80%91%E8%90%A5%E9%94%80%E6%B4%BB%E5%8A%A8%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx"
    url = "https://cdn.smartpushedm.com/material_ec2_prod/2025-03-06/fe6f042f50884466979155c5ef825736/copy%20of%202025-01-16%20%E5%88%9B%E5%BB%BA%E7%9A%84%20A%2FB%20%E6%B5%8B%E8%AF%95%20copy%20of%202025-01-16%20app-%E6%99%AE%E9%80%9A%E6%A8%A1%E6%9D%BF%201%E6%95%B0%E6%8D%AE%E6%80%BB%E8%A7%88.xlsx"

    # e_person_oss1 = "https://cdn.smartpushedm.com/material_ec2/2025-02-27/b48f34b3e88045d189631ec1f0f23d51/%E5%AF%BC%E5%87%BA%E5%85%A8%E9%83%A8%E5%AE%A2%E6%88%B7.csv"
    # a_person_oss2 = "https://cdn.smartpushedm.com/material_ec2/2025-02-27/c50519d803c04e3b9b52d9f625fed413/%E5%AF%BC%E5%87%BA%E5%85%A8%E9%83%A8%E5%AE%A2%E6%88%B7.csv"

    # # #actual_oss= get_oss_address_with_retry("23161","https://cdn.smartpushedm.com/material_ec2_prod/2025-02-20/dae941ec20964ca5b106407858676f89/%E7%BE%A4%E7%BB%84%E6%95%B0%E6%8D%AE%E6%A6%82%E8%A7%88.xlsx","",'{"page":1,"pageSize":10,"type":null,"status":null,"startTime":null,"endTime":null}')
    # # res=read_excel_and_write_to_dict(read_excel_from_oss(actual_oss))
    # # print(res)
    # # print(read_excel_and_write_to_dict(read_excel_from_oss(oss1), type=".xlsx"))
    # print(check_excel(check_type="all", actual_oss=actual_oss, expected_oss=expected_oss))
    # print(check_excel_all(actual_oss=oss1, expected_oss=oss2,skiprows =1))
    # print(check_excel_all(actual_oss=oss1, expected_oss=oss2,ignore_sort=True))
    # print(check_excel_all(actual_oss=a_person_oss2, expected_oss=e_person_oss1, check_type="including"))
    print(ExcelExportChecker.check_excel_all(actual_oss=oss3, expected_oss=oss4, check_type="including"))
    # read_excel_csv_data(type=)
    # print(DataTypeUtils().check_email_format())
    # errors = ExcelExportChecker.check_field_format(actual_oss=oss1, fileds={0: {5: "time"}}, skiprows=1)
    # ExcelExportChecker.check_excel_name(actual_oss=oss1, expected_oss=url)

    _url = "http://sp-go-flow-test.inshopline.com"
    params = {
        "abandonedOrderId": "c2c4a695a36373f56899b370d0f1b6f2",
        "areaCode": "",
        "context": {
            "order": {
                "buyerSubscribeEmail": True,
                "checkoutId": "c2c4a695a36373f56899b370d0f1b6f2",
                "discountCodes": [],
                "orderAmountSet": {
                    "amount": 3,
                    "currency": "JPY"
                },
                "orderDetails": [
                    {
                        "productId": "16060724900402692190790343",
                        "title": "测试2.0-商品同步AutoSync-2023-08-17 20:52:00",
                        "titleTranslations": []
                    }
                ],
                "receiverCountryCode": "HK"
            },
            "user": {
                "addresses": [],
                "areaCode": "",
                "email": "testsmart200+10@gmail.com",
                "firstName": "testsmart200+10",
                "gender": "others",
                "id": "1911625831177650177",
                "lastName": "",
                "phone": "",
                "tags": [],
                "uid": "4603296300",
                "userName": "testsmart200+10"
            }
        },
        "controlObjectId": "c2c4a695a36373f56899b370d0f1b6f2",
        "controlObjectType": 4,
        "email": "testsmart200+10@gmail.com",
        "handle": "smartpush4",
        "language": "en",
        "messageId": "1911625832100397058",
        "phone": "",
        "platform": 4,
        "storeId": "1644395920444",
        "timezone": "Asia/Macao",
        "triggerId": "c1001",
        "uid": "4603296300",
        "userId": "1911625831177650177"
    }
    mock_pulsar = MockFlow.mock_pulsar(_url, params)
