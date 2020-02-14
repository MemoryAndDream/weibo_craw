# weibo_craw

三个程序入口对应三种不同需求
weibo/just_comments.py # 单条博文采集评论
weibo/weibo_by_hour.py  # 按小时拆分高级搜索条件采集 字段包括发布时间，博文，评论数，转发数，点赞数等
weibo/main.py  # 按日拆分高级搜索条件采集
 
 
需要修改的部分：
chromedriver.exe 路径。 你需要下载你自己的chrome浏览器对应版本的驱动参考 https://blog.csdn.net/BinGISer/article/details/88559532
抓取评论最好需要代理，这个注释掉了
默认使用用户默认浏览器文件夹，因此运行前需要用chrome浏览器登录下微博，然后运行前需要关闭所有chrome浏览器
