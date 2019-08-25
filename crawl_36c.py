import json
import requests
import time
from lxml import etree
import os
from urllib.parse import parse_qs


# 登录后的Cookie信息
headers = {
    'Cookie': 'SINAGLOBAL=7158709706582.449.1555079844464; __guid=15428400.1270704228271856000.1557997231765.4236; UOR=www.mobiletrain.org,widget.weibo.com,www.so.com; YF-V5-G0=7e17aef9f70cd5c32099644f32a261c4; WBStorage=edfd723f2928ec64|undefined; login_sid_t=0d1034bea57cf3495c86ae26ebd6160d; cross_origin_proto=SSL; Ugrow-G0=7e0e6b57abe2c2f76f677abd9a9ed65d; _s_tentry=weibo.com; wb_view_log=1920*10801; Apache=8085569108657.615.1564627374908; ULV=1564627374913:6:1:1:8085569108657.615.1564627374908:1559102250032; SCF=AnlOTBA5OkVt9EE85lpG3K2-pSxxnxnNl0kUWGILL95Iikeyes-CKD-VUujcvLarO9g_-PLdPJAQzZuCRJTcL2E.; SUB=_2A25wRiIyDeRhGeBP61QW9ifLyj6IHXVTMhT6rDV8PUNbmtBeLRPRkW9NRXM-8JQMM51ucaec0zYSytvevug-dp3V; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFCkHC7VLYI.SHHddzIe1lv5JpX5KzhUgL.FoqpehqNSo.NeKz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMceK5cS0q4S02E; SUHB=0KAxjp5sdWrn8Q; ALF=1596163554; SSOLoginState=1564627554; wvr=6; wb_view_log_6106769712=1920*10801; monitor_count=7; YF-Page-G0=e57fcdc279d2f9295059776dec6d0214|1564627650|1564627471; webim_unReadCount=%7B%22time%22%3A1564627597760%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A35%2C%22msgbox%22%3A0%7D',
}
# 当前路径+pic
pic_file_path = os.path.join(os.path.abspath(''), '36C_pic')


# 下载图片
def download_pic(url, nick_name):
    if not url:
        return
    if not os.path.exists(pic_file_path):
        os.mkdir(pic_file_path)
    resp = requests.get(url)
    if resp.status_code == 200:
        with open(pic_file_path + f'/{nick_name}.jpg', 'wb') as f:
            f.write(resp.content)


if __name__ == '__main__':
    params = {
        'ajwvr': 6,
        'id': '4367970740108457',
        'from': 'singleWeiBo',
        'root_comment_max_id': ''
    }
    URL = 'https://weibo.com/aj/v6/comment/big'
    # 爬去100页，需要代理，或者进行sleep 不然会超时。
    for num in range(101):
        time.sleep(2)
        print(f'=========   正在读取第 {num} 页 ====================')
        # resp = requests.get(URL, params=params, headers=headers, proxies={"http": random.choices(proxies)[0]})
        resp = requests.get(URL, params=params, headers=headers)
        resp = json.loads(resp.text)
        if resp['code'] == '100000':
            html = resp['data']['html']

            html = etree.HTML(html)
            max_id_json = html.xpath('//div[@node-type="comment_loading"]/@action-data')[0]

            node_params = parse_qs(max_id_json)
            # max_id
            max_id = node_params['root_comment_max_id'][0]
            params['root_comment_max_id'] = max_id
            # data = html.xpath('//div[@class="list_ul"]/div[@node-type="root_comment"]/div[@class="list_con"]')
            data = html.xpath('//div[@node-type="root_comment"]')
            for i in data:
                # 评论人昵称
                nick_name = i.xpath('.//div[@class="WB_text"]/a/text()')[0]
                # 评论内容。
                # test = i.xpath('.//div[@class="WB_text"]/text()')
                wb_text = i.xpath('.//div[@class="WB_text"][1]/text()')
                string = ''.join(wb_text).strip().replace('\n', '')
                # 评论id , 用于获取评论内容
                comment_id = i.xpath('./@comment_id')[0]
                # 评论的图片地址
                pic_url = i.xpath('.//li[@class="WB_pic S_bg2 bigcursor"]/img/@src')
                pic_url = 'https:' + pic_url[0] if pic_url else ''
                print(pic_url)
                download_pic(pic_url, nick_name)