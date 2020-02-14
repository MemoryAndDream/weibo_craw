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
    start_date = '2019-12-01'
    end_date = '2020-01-01'
    cop = ChromeOperate(executable_path=r'F:\work\py3_pj\amazon_craw\chromedriver.exe')
    date_list = dateRange(start_date, end_date)
    print(date_list)
    search_url_template = 'https://s.weibo.com/weibo?q=%E5%8D%8E%E4%B8%BA%20-%E5%96%9C%E9%A9%AC%E6%8B%89%E9%9B%85&scope=ori&typeall=1&suball=1&timescope=custom:{0}-{1}:{2}-{3}&Refer=SWeibo_box'
    line = ['时间', '博文id','用户', '用户id', '评论', '转发', '点赞', '博文']
    hours=[
        [0,2],
        [2, 4],
        [4, 6],
        [6, 8],
        [8, 10],
        [10, 12],
        [12, 14],
        [14, 16],
        [16, 18],
        [18, 20],
        [20, 22],
        [22, 23]
    ]
    yield line
    for i in range(len(date_list)-1):
        for hour in hours:
            start_date = date_list[i]
            end_date = date_list[i+1]
            print(start_date)
            shour,ehour = hour[0],hour[1]
            search_url = search_url_template.format(start_date,shour,start_date,ehour)
            cop.open(search_url)
            for page_num in range(5):
                try:
                    page_buf = cop.open_source()
                    posts = ct.getXpath('//div[@class="card-wrap"]',page_buf)
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
                        user_id =  ct.getXpath1('//a[@class="name"]/@href',post)
                        user_id = ct.getRegex('weibo.com/(\d+)',user_id)
                        mid = ct.getXpath1('//div/@mid',post)
                        ''
                        # 评论
                        comments_button = ct.getXpath1('//a[@action-type="feed_list_comment"]/text()',post)
                        comments_count = ct.getRegex('评论 (\d+.*)', comments_button)
                        if not comments_count:
                            comments_count = 0
                        # get_comments = []
                        feed_list_forward_button = ct.getXpath1('//a[@action-type="feed_list_forward"]/text()', post)
                        forward_count = ct.getRegex('转发 (\d+.*)', feed_list_forward_button)
                        if not forward_count:
                            forward_count=0

                        like_button = ct.getXpath('//a[@action-type="feed_list_like"]', post)
                        if like_button:
                            like_button =like_button[-1]
                            like_button = ct.getXpath1("//em/text()",like_button)
                            like_count = ct.getRegex('(\d+.*)', like_button)
                            if not like_count:
                                like_count = 0
                        else:
                            like_count = 0

                        # feed_list_forward  # 转发

                        # if ct.getRegex('评论 (\d+.*)',comments_button):
                        #                     #     try:
                        #                     #         # proxy = ct.get_new_1min_proxy()
                        #                     #         # proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
                        #                     #         # try:
                        #                     #         #     comments_page = ct.get('https://m.weibo.cn/api/comments/show?id='+mid,proxies=proxies) # 获取评论会封ip，另外有很多评论不可见(敏感词，用户设置) 虽然评论数不是空
                        #                     #         # except:
                        #                     #         #     time.sleep(2)
                        #                     #         time.sleep(2)
                        #                     #         comments_page = ct.get('https://m.weibo.cn/api/comments/show?id=' + mid)
                        #                     #         json_data = json.loads(comments_page)
                        #                     #         comments = json_data['data']['data']
                        #                     #         for comment in comments:
                        #                     #             comment_text = comment['text']
                        #                     #             get_comments.append(comment_text)
                        #                     #     except Exception as e:
                        #                     #         print(e,mid)


                        line = [date,mid,nick,user_id,comments_count,forward_count,like_count,texts]
                        yield line

                    next_button = cop.find_elements_by_xpath('//a[@class="next"]')
                    if next_button:
                        time.sleep(random.randint(2, 4))
                        next_button[0].click()
                    else:
                        break
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    data = weibo_search()
    ct.writer_to_csv(data,'weibo.csv')

