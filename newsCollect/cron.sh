#! /bin/sh
export PATH=$PATH:/usr/local/bin

# 爬虫项目目录 新的部署需要更改路径
cd /root/projects/NewsCollect/newsCollect/
source ../env/bin/activate
rm -rf .scrapy
nohup python3 schedule.py > schedule.log 2>&1 &

# crontab部署命令
# crontab -e
# 0 * * * * sh /root/projects/NewsCollect/newsCollect/cron.sh