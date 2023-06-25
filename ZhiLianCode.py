import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import ConnectionMongodb


def get_html(url, params):
    my_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Cookie": "adfbid2=0; x-zp-client-id=e616e198-8a50-40be-ae27-5c79c62127bb; urlfrom2=121113803; sts_deviceid=188e46d34c35d3-00053b2b549984-26031d51-2073600-188e46d34c411b4; ZP_OLD_FLAG=false; campusOperateJobUserInfo=62bec016-ce4a-40a6-8177-f5eec8dc562c; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; at=790d7c2afecc4b94ba9e72a1e69dc6a0; rt=22559a838f59488797b0cb13c67756a5; FSSBBIl1UgzbN7NO=5TlUVEQMVEVVxuHucK9NGhY.BtntJOayI0nr560NLkaBZgAIYsFaBUNA4KWAL3lilXw01PWqijiFtvWgXVV9doG; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221172601999%22%2C%22first_id%22%3A%221872cb849b8281-0d8d4f271eb121-26031851-2073600-1872cb849b9fd8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22baidupcpz%22%2C%22%24latest_utm_medium%22%3A%22cpt%22%2C%22%24latest_utm_campaign%22%3A%22jl%22%2C%22%24latest_utm_content%22%3A%22tj%22%2C%22%24latest_utm_term%22%3A%2232712949%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTg3MmNiODQ5YjgyODEtMGQ4ZDRmMjcxZWIxMjEtMjYwMzE4NTEtMjA3MzYwMC0xODcyY2I4NDliOWZkOCIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjExNzI2MDE5OTkifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221172601999%22%7D%2C%22%24device_id%22%3A%221872cb849b8281-0d8d4f271eb121-26031851-2073600-1872cb849b9fd8%22%7D; locationInfo_search={%22code%22:%22771%22%2C%22name%22:%22%E8%8C%82%E5%90%8D%22%2C%22message%22:%22%E5%8C%B9%E9%85%8D%E5%88%B0%E5%B8%82%E7%BA%A7%E7%BC%96%E7%A0%81%22}; _uab_collina=168752064970486138187739; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1687459544,1687520650; ssxmod_itna=YqIOqUx0xG2G8DzxAxeTj4jrhRtWP+PitrqT7DlaoxA5D8D6DQeGTr2T=IQqNQCbZwDIrq7j4YR33zWocYeYbhmxIYDU4i8DCuiePrDeW=D5xGoDPxDeDAWqGaDb4DrRPqGpc2Lss1OD3qDwDB=DmqG2DlNDA4DjFTwsFwt6QeiexGt4AL+3FqDMD7tD/SxbO7=DGLnTOiNSBnTDbopRYmiDtqD9FWtUieDHCwNMekFTIYpT+03=+BhaYGErI0hQiO+xf0GEvDxTf7DPYBhQKYqoU0gIxDf48KqxD===; ssxmod_itna2=YqIOqUx0xG2G8DzxAxeTj4jrhRtWP+PitrqTD6hFrmx0HPquq03kenjXD6WrXNh9eHZKlk0AClfmC5xCafiQBtenKiQSN=nzm=ur0YYt0vTKnKXLlrPEo8BymGf5B9EacNpdzfg5cA58DOmzGxWz0aq+XgetDhwzKgWbc15xnrKa9c7Py1ivWar=l7aN/GD3DQKqUD08DYKq4D==; ZL_REPORT_GLOBAL={%22jobs%22:{%22funczoneShare%22:%22dtl_best_for_you%22}}; selectCity_search=538; FSSBBIl1UgzbN7NP=5RxMifD1KuLWqqqDE41hNpqKstIAdFjHAM_olFjQcwg5WcejHQepGk61RpdPmotrwRlOeZqwzLUyAq218uXOJ_0.zESQL7mIBE3ltiQFVNe4.YEevfl5kvbE5HUqGzw9NZEDN0l.V7_sV.Ek8oj7gyHYGsTBILMXxVQQHNsTzlfh_ONE0WWIfBYNQfPWVY1dj1vR3b4MJ1nch7FK2omvFPPt9Dfh.x45qP6udqBuRwtbcywyRZFcbCnNzkcskNV59PDKy7YysZIkYqkltdEMcG1wo3C7gMWcx_Sgl.bRadO.z_Bnpy5sodybQkDg3XZYUqsGHA517skZ3tEnroAX6vC"
    }
    req = requests.get(url, headers=my_headers, params=params)
    req.encoding = req.apparent_encoding
    html = req.text
    return html


def get_html_list(url, city_num):
    html_list = []
    # 每页最多34页
    for i in range(1, 33):
        params = {'jl': str(city_num), 'kw': 'java', 'p': str(i)}
        html = get_html(url, params)
        soup = BeautifulSoup(html, 'html.parser')
        html_list += soup.find_all(name='a', attrs={'class': 'joblist-box__iteminfo iteminfo'})
    for i in range(len(html_list)):
        html_list[i] = str(html_list[i])
    return html_list


def get_data(html_list):
    for i in html_list:
        data_SUM = {}
        print("正在爬取")
        if re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i):
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(1)
            # data_SUM.append(s)
            data_SUM["name"] = s
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(2)
            data_SUM["year"] = s
            s = re.search(
                '<li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li> <li class="iteminfo__line2__jobdesc__demand__item">(.*?)</li>',
                i).group(3)
            data_SUM["xueli"] = s
        else:
            data_SUM["name"] = ""
            data_SUM["year"] = ""
            data_SUM["xueli"] = ""
        if re.search('<span class="iteminfo__line1__jobname__name" title="(.*?)">', i):
            s = re.search('<span class="iteminfo__line1__jobname__name" title="(.*?)">', i).group(1)
            data_SUM["zhiwei"] = s
        else:
            data_SUM["zhiwei"] = ""

        if re.search('<span class="iteminfo__line1__compname__name" title="(.*?)">', i):
            s = re.search('<span class="iteminfo__line1__compname__name" title="(.*?)">', i).group(1)
            data_SUM["gongsi"] = s
        else:
            data_SUM["gongsi"] = ''

        if re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i):
            s = re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i).group(1)
            data_SUM["xingzhi"] = s
            s = re.search(
                '<span class="iteminfo__line2__compdesc__item">(.*?) </span> <span class="iteminfo__line2__compdesc__item">(.*?) </span>',
                i).group(2)
            data_SUM["peoples"] = s
        else:
            data_SUM["xingzhi"] = ''
            data_SUM["peoples"] = ''
        if re.search('<p class="iteminfo__line2__jobdesc__salary">([\s\S]*?)<', i):
            s = re.search('<p class="iteminfo__line2__jobdesc__salary">([\s\S]*?)<', i).group(1)
            s = s.strip()
            data_SUM["money"] = s
        else:
            data_SUM["money"] = ''

        s = str()
        l = re.findall('<div class="iteminfo__line3__welfare__item">.*?</div>', i)
        for i in l:
            s = s + re.search('<div class="iteminfo__line3__welfare__item">(.*?)</div>', i).group(1) + ' '
        data_SUM["content"] = s
        print(data_SUM)
        # 插入数据
        connection.insert_one(data_SUM)

if __name__ == '__main__':

    url_ttt = 'https://sou.zhaopin.com/?'
    # citys = {'上海': 538, '北京': 530, '广州': 763, '深圳': 765, '天津': 531, '武汉': 736, '西安': 854, '成都': 801, '南京': 635,}
    citys = {
        '杭州': 653
    }
    # 连接mongodb
    connection = ConnectionMongodb.connection()
    for i in citys.keys():
        print("爬取" + str(i))
        html_list = get_html_list(url_ttt, citys[i])
        get_data(html_list)
