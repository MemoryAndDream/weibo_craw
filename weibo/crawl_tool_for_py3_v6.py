# -*- coding: utf-8 -*-
"""
File Name：     crawl_tool_for_py3
Description :
Author :       meng_zhihao
date：          2018/11/20
"""

import requests
from lxml import etree
import re

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

#通用方法
class crawlerTool:

    def __init__(self):
        self.session = requests.session()
        self.proxy_now = ''
        pass

    def __del__(self):
        self.session.close()

    @staticmethod
    def get(url, proxies=None, cookies={}, referer='',headers={}):
        if not headers:
            if referer:
                headers = {'Referer': referer}
                headers.update(HEADERS)
            else:
                headers = HEADERS
        if proxies:
            rsp = requests.get(url, timeout=10, headers=headers, cookies=cookies,proxies=proxies)
        else:
            rsp = requests.get(url, timeout=30, headers=headers, cookies=cookies)
        return rsp.content  # 二进制返回

    @staticmethod
    def post(url,data,headers={}): # 必须传入字典，中文不用编码！
        if headers:
            rsp = requests.post(url, data, timeout=10,headers=headers)
        else:
            rsp = requests.post(url,data,timeout=10)
        return rsp.content


    def sget(self,url,cookies={},headers = {}):
        headers = headers.update(HEADERS)
        if cookies:
            rsp = self.session.get(url,timeout=10,headers=headers,cookies=cookies)
        else:
            rsp = self.session.get(url, timeout=10, headers=headers)
        return rsp.content # 二进制返回

    def spost(self,url,data,allow_redirects=True,headers = {}):
        headers = headers.update(HEADERS)

        rsp = self.session.post(url,data,timeout=10,headers=headers,allow_redirects=allow_redirects)
        return rsp.content



    # 获取xpath 要判断一下输入类型，或者异常处理
    @staticmethod
    def getXpath(xpath, content):   #xptah操作貌似会把中文变成转码&#xxxx;  /text()变unicode编码
        tree = etree.HTML(content)
        out = []
        results = tree.xpath(xpath)
        for result in results:
            if  'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)) :
                out.append(result)
            else:
                out.append(etree.tostring(result))
        return out

    # 获取xpath 要判断一下输入类型，或者异常处理
    @staticmethod
    def getXpath1(xpath, content):   #python3的xpath传入的应该是字符串！！
        tree = etree.HTML(content)
        out = []
        results = tree.xpath(xpath)
        for result in results:
            if  'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)) :
                out.append(result)
            else:
                out.append(etree.tostring(result))
        if out:
            return out[0]
        return ''

    @staticmethod
    def getRegex(regex, content):
        if type(content) == type(b''):
            content = content.decode('utf8')
        rs = re.search(regex,content)
        if rs:
            return rs.group(1)
        else:
            return ''

    @staticmethod
    def parser_urlpars(pars):
        # pars= 'q=GENER8%20MARITIME%2C%20INC.&quotesCount=6&newsCount=4&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_cie_vespa&enableCb=true&enableNavLinks=true&vespaNewsTimeoutMs=600'
        from urllib.parse import quote, unquote
        pars = pars.replace('+', ' ')
        field_pars = pars.split('&')
        par_dict = {}
        for field_par in field_pars:
            field = field_par.split('=')
            if len(field) == 1:
                par_dict[unquote(field[0])] = None
            else:
                par_dict[unquote(field[0])] = unquote(field[1])
        return par_dict

    @staticmethod
    def parser_cookie(cookie_str):
        # cookie_str = '_vcooline_ikcrm_production_ikcrm.com_session_=bHpKZVZSUzNoZ3MraFVBK1BrV1MvbjF1Mzdtdk9lZ0pxWm0zY1hUVDRnVXhBWTNmek9pQ2xNelJFRE1obVRoaVg4RkJldU5JR0xrKzNUSE5RUWxTWU5DSlVRVjBtTkhrMmJWMzRDTjJ3MXNhQjVwSjlsZkRsRjJYR0FUbERhdWtNdEhrM1V5emdBd1VzN0FIR0ppOTNYZjNGSHJ0cjVCcmJBVXhPdVFCdWkyeTF6b0RiRFA3ZVV0VWRNelQ5NHIweWsxSkxRSkRWbTUxaHBKaGFnc1NlSEl1MjZnQUFBdDhXUm8xV3pYWmcwVTVCbnpkT0tpNlNOZlVUdEUzUUo4YlhVelBBMkhyL3QzR0hHenpiM0hnVzZickMzTDBvMTBvNkFhenNJOWZxTGMyQk9VUnl3aVV2ellzZ05HeGZ2L1EtLUhwOWNLZEwxWm5xN0M5TjhxL2JpQVE9PQ%3D%3D--7085cd9bc2c7ff4f2e1f60bf29a838f21ef41ede; domain=.ikcrm.com; path=/'
        cookie_dict = {}
        for cookie in cookie_str.split(';'):
            l = cookie.split('=')
            key, value = l[0],'='.join(l[1:])
            cookie_dict[key] = value
        return cookie_dict

    @staticmethod
    def get_text(page_source):
        if type(page_source) == type(b''):
            page_source = page_source.decode('utf8')
        return re.sub('(<.*?>)',"",page_source)

    @staticmethod
    def quote(input):
        from urllib import parse
        return parse.quote(input)

    @staticmethod
    def unquote(input):
        from urllib import parse
        return parse.unquote(input)

    def thread_get(self):

        pass

    @staticmethod
    def get_new_5min_proxy():
        '''curl 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=101&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Referer: http://www.zhilianhttp.com/getapi.html' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: PHPSESSID=62eeapps46ucvcbg4qbqir15u6; SERVERID=fe3e577c4710ab81a140ce46bb723b00|1566458695|1566456808' --compressed'''
        # 网站有反爬虫 请自行去http://www.zhilianhttp.com/Shop/index.html?on=exclusive购买代理账号，充值代理币，然后提取5分钟的代理 这里用的是我的账号 但是白名单是我自己的ip  或者加大延时！ http://www.zhilianhttp.com
        import requests
        url = 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=101&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson='
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
        cookies = {"PHPSESSID": "0pio7gtq035godm163mnplllo5",
                   "SERVERID": "5e4e1bec6f8aa1c7027d0867db140981|1566534695|1566534695"}  # 这里替换成自己的账号cookie！
        proxy = requests.get(url, timeout=10, headers=HEADERS, cookies=cookies).text
        return proxy.strip()


    @staticmethod
    def get_new_1min_proxy():
        '''curl 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=101&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Referer: http://www.zhilianhttp.com/getapi.html' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9' -H 'Cookie: PHPSESSID=62eeapps46ucvcbg4qbqir15u6; SERVERID=fe3e577c4710ab81a140ce46bb723b00|1566458695|1566456808' --compressed'''
        # 网站有反爬虫 请自行去http://www.zhilianhttp.com/Shop/index.html?on=exclusive购买代理账号，充值代理币，然后提取5分钟的代理 这里用的是我的账号 但是白名单是我自己的ip  或者加大延时！ http://www.zhilianhttp.com
        import requests
        url = 'http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=100&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson=&usertype=2'
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
        cookies = {"PHPSESSID": "0pio7gtq035godm163mnplllo5",
                   "SERVERID": "5e4e1bec6f8aa1c7027d0867db140981|1566534695|1566534695"}  # 这里替换成自己的账号cookie！
        proxy = requests.get(url, timeout=10, headers=HEADERS, cookies=cookies).text
        return proxy.strip()


    def get_by_proxy(self,url,success_symbol = '',failed_symbol_symbol='',cookies={}, referer=''):
        '''

        :param success_symbol:  访问成功的标志
        :param failed_symbol_symbol:  访问失败的标志
        :return:
        '''
        page_buf = ''
        for retry_times in range(2):
            if not self.proxy_now:
                self.proxy_now = self.get_new_1min_proxy()
            page_buf = self.get(url,referer=referer,cookies=cookies,proxies = {'http':'http://'+self.proxy_now ,'https':'http://'+self.proxy_now }).decode('utf8')
            if success_symbol and success_symbol in page_buf:
                return page_buf
            if failed_symbol_symbol in page_buf:
                continue
            return page_buf

    def get_regular_file_name(self,file_name):
        file_name = file_name.replace('\t','').replace('\n','')
        file_name = re.sub(u"([/\\\\:*?<>|])", "", file_name)
        return file_name


    @staticmethod
    def writer_to_csv(datas,file_path):
        import csv
        with open(file_path,'a',encoding='utf_8_sig',newline='',) as fout:
            writer = csv.writer(fout)
            for data in datas:
                writer.writerow(data)
                fout.flush()








if __name__ == '__main__':
    # content = (crawlerTool.get('http://docs.python-requests.org/zh_CN/latest/user/quickstart.html'))
    # content = (content.decode('utf8'))
    # print(crawlerTool.getXpath('//h2/text()',content))
    # ctobj = crawlerTool()
    # # ctobj.sget('https://www.ic.net.cn/')
    # #
    # p = crawlerTool.get('https://www.amazon.com/gp/search/other/ref=sr_in_A_B?rh=i%3Afashion-mens-clothing%2Cn%3A7141123011%2Cn%3A%217141124011%2Cn%3A7147441011%2Cn%3A1040658%2Cn%3A2476517011%2Ck%3At-shirt&keywords=t-shirt&pickerToList=enc-merchantbin&indexField=A&ie=UTF8&qid=1572916359')
    # print(p)
    # with open('1.html','w') as f:
    #     f.write(p.decode('utf8'))
    # print(ctobj.get_new_5min_proxy())
    # p = crawlerTool.get('http://www.google.com/',proxies={'http':'socks5://'+'127.0.0.1:1080','https':'socks5://'+'127.0.0.1:1080'}) # pip install pysocks
    # print(p)
#     # import binascii
#     # with open('28099.html',encoding='utf8') as f:
#     #     page = f.read()
#     #     contents = crawlerTool.getXpath('//span[@class="stonefont"]/text()',page)
#     #     for content in contents:
#     #         print(content)
#     #         byte_data = content.encode('utf8')  # 7 24494 74.09  '\xef\x8b\x81' 7 \xef\x8f\xa5 4  xee\x8a\x80 2
#     #         print(byte_data)
#     #         print(binascii.b2a_hex(byte_data)
# )
    print(crawlerTool().get_new_1min_proxy())

