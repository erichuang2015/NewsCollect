# 工大新闻站
## 项目概况
该项目是一个基于Scrapy和Flask的网页爬虫及前端，目的在于增量地收集合工大所有网站新闻信息并集中呈现

## 技术栈
项目分为两个模块：
- Scrapy爬虫
- Flask应用

由于复杂度不高，以及一些目前尚不清楚原因的bug，Flask应用只使用了单一文件。在后续需求增加的情况下会重新使用Blueprint构建Flask应用。

### 爬虫
#### 爬取逻辑
爬虫从info文件获取相应网站相关信息。这些信息包括：
- 不同板块的url模板
- 不同板块的tag

并且提供了辅助函数`render_url()`渲染url模板。

具体的info信息参见info.py。

具体抓取逻辑可以自由定义，需要抓取的内容参见items.py中的定义

#### 在此提供一个通用的爬取逻辑：

提取不同版面url模板并将变量部分写入info

-> 以不同版面第一页作为start_url

-> 提取页码部分

-> 根据config中的爬取页数将其他页面呈递到下一级parser

-> 从页面中提取新闻列表，获取title和time

-> 提取新闻内容并使用提供的`content_process()`函数取得修饰过的可储存HTML内容

> 该存储用于后期对于内容修饰及独立显示，目前由于css原因新闻站链接到原地址

-> 赋值给item

#### 增量爬取
使用redis实现增量去重，构建基于redis的pipeline
#### 定时爬取
使用crontab实现定时执行任务

## 环境依赖
### 外部环境依赖
- mysql
- redis
### 内部环境依赖
- python >= 3.5.X
- requirments.txt
> Twisted在python3下无法使用pip正常安装，需要源码编译


## 项目部署
### 环境变量
需要添加mysql用户密码到环境变量
### 爬虫模块
爬虫模块采用corntab实现定时爬取
#### crontab部署命令
```
crontab -e
0 * * * * sh $projectPath$/NewsCollect/newsCollect/cron.sh
```
#### Config
爬虫模块使用json作为config文件，其中记录了爬虫配置以及数据库配置




