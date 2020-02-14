# -*- coding: utf-8 -*-
"""
File Name：     main
Description :
Author :       meng_zhihao
mail :       312141830@qq.com
date：          2020/2/4
"""

import datetime
import time
from selenium_operate import ChromeOperate
from crawl_tool_for_py3_v6 import crawlerTool as ct
import random
import json

def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def weibo_search():
    # start_date = '2020-01-10' # 10-12
    start_date = '2020-01-10'
    end_date = '2020-02-12'
    cop = ChromeOperate(executable_path=r'F:\work\py3_pj\amazon_craw\chromedriver.exe')
    date_list = dateRange(start_date, end_date)
    print(date_list)
    search_url_template = 'https://s.weibo.com/weibo/%25E6%2594%25BF%25E5%25BA%259C?q=whzf&scope=ori&suball=1&timescope=custom:{0}-0:{1}-0&Refer=g'

    for i in range(len(date_list)-1):
        start_date = date_list[i]
        end_date = date_list[i+1]
        search_url = search_url_template.format(start_date,end_date)
        cop.open(search_url)
        for page_num in range(50):
            try:
                page_buf = cop.open_source()
                posts = ct.getXpath('//div[@class="card-wrap"]',page_buf)
                proxy = ct.get_new_1min_proxy()
                proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
                for post in posts:
                    texts = ct.getXpath('//p[@node-type="feed_list_content_full"]//text()',post)
                    if not texts:
                        texts = ct.getXpath('//p[@node-type="feed_list_content"]//text()', post)
                    texts = ''.join(texts)
                    if not texts:
                        continue
                    date = ""
                    from_source = ct.getXpath('//p[@class="from"]',post)
                    if from_source:
                        date = ct.getXpath1('//a/text()', from_source[-1])
                        date = date.strip()
                    nick = ct.getXpath1('//a/@nick-name',post)
                    mid = ct.getXpath1('//div/@mid',post)
                    ''
                    # 评论
                    comments_button = ct.getXpath1('//a[@action-type="feed_list_comment"]/text()',post)
                    get_comments = []
                    if ct.getRegex('评论 (\d+.*)',comments_button):
                        try:

                            try:
                                comments_page = ct.get('https://m.weibo.cn/api/comments/show?id='+mid,proxies=proxies) # 获取评论会封ip，另外有很多评论不可见(敏感词，用户设置) 虽然评论数不是空
                                json_data = json.loads(comments_page)
                                comments = json_data['data']['data']
                                for comment in comments:
                                    comment_text = comment['text']
                                    get_comments.append(comment_text)
                            except:
                                time.sleep(2)
                                proxy = ct.get_new_1min_proxy()

                            # time.sleep(2)
                            # comments_page = ct.get('https://m.weibo.cn/api/comments/show?id=' + mid)
                            # json_data = json.loads(comments_page)
                            # comments = json_data['data']['data']
                            # for comment in comments:
                            #     comment_text = comment['text']
                            #     get_comments.append(comment_text)
                        except Exception as e:
                            print(e,mid)

                    line = [date,mid,nick,texts]+get_comments
                    yield line

                next_button = cop.find_elements_by_xpath('//a[@class="next"]')
                if next_button:
                    time.sleep(random.randint(1, 2)*0.6)
                    next_button[0].click()
                else:
                    break
            except Exception as e:
                print(e)


if __name__ == '__main__':
    data = weibo_search()
    ct.writer_to_csv(data,'武汉政府.csv')

