# 工大新闻站部署说明
## 环境依赖
### 外部环境依赖
- mysql
### 内部环境依赖
- python >= 3.5.X
- requirments.txt
> Twisted在python3下无法使用pip正常安装，需要源码编译

## 项目部署
### 爬虫模块
爬虫模块采用corntab实现定时爬取
#### crontab部署命令
```
crontab -e
0 * * * * sh $projectPath$/NewsCollect/newsCollect/cron.sh
```
#### Config
爬虫模块使用json作为config文件，其中记录了爬虫配置以及数据库配置


