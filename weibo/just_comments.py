# -*- coding: utf-8 -*-
"""
File Name：     just_comments
Description :
Author :       meng_zhihao
mail :       312141830@qq.com
date：          2020/2/11
"""
from selenium_operate import ChromeOperate
from crawl_tool_for_py3_v6 import crawlerTool as ct
import time
def main():
    cop = ChromeOperate(executable_path=r'F:\work\py3_pj\amazon_craw\chromedriver.exe')
    url = 'https://m.weibo.cn/status/4470730772817031'
    cop.open(url)
    while True:
        time.sleep(1)
        cop.down_page()
        page_buf = cop.open_source()
        comments = ct.getXpath('//h3/text()',page_buf)
        comments =[[text] for text in comments]
        ct.writer_to_csv(comments,'comments.csv')

if __name__ == '__main__':
    main()