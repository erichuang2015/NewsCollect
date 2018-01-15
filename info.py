# -*- coding: utf-8 -*-

info = {
    'hfut': {
        'unit': '工大官网',
        'url_template': 'http://news.hfut.edu.cn/list-[tag_code]-[page].html',
        'tag_codes': {
            '1': '工大要闻',
            '2': '通知公告',
            '28': '报告讲座',
            '7': '综合新闻',
            '161': '教学科研',
            '162': '合作交流',
            '4': '工大人物',
            '5': '校友风采',
            '8': '多彩校园',
            '16': '教育视点',
            '17': '科技视点',
            '3': '招标采购',
        }
    },
    'jxgc': {
        'unit': '机械工程学院',
        'url_template': 'http://jxxy.hfut.edu.cn/index.php/cn/xwgg/[primary_title]',
        'tag_codes': {
            'news1': {
                'tzgg1': '学院通告',
                'tzgg2': '科研公告',
                'tzgg3': '研究生培养公告',
                'tzgg4': '本科教育通知',
                'tzgg5': '党建公告',
            },
            'news2': '学院新闻',
            'news3': '科研信息',
        }
    },
    'CI': {
        'unit': '计算机与信息学院',
        'url_template': 'http://ci.hfut.edu.cn/[tag_code]/list[page].htm',
        'tag_codes': {
            '3961': '通知公告',
            '3962': '学院新闻',
            'xsdtzd': '学术动态',
            '3965': '教学信息',
        },
    },
    'EA': {
        'unit': '电气与自动化工程学院',
        'url_template': 'http://ea.hfut.edu.cn/ea/index.php/cn/ea-news/[tag_code]',
        'tag_codes': {
            'ea-news-zh': '学院新闻',
            'announcements-zh': '通知公告',
            'ea-academic': '学术动态',
            'ea-photonews': '精选图文',
        },
    },
    'MSE': {
        'unit': '材料科学与工程学院',
        'url_template': 'http://mse.hfut.edu.cn/[tag_code]/list[page].htm',
        'tag_codes': {
            '3564': '学院新闻',
            '3565': '通知公告',
            '3549': '科研动态',
        },
        'rules': {
            'url_template': 'http://mse.hfut.edu.cn/[tag_code]/list[page].htm',
            'base_url': 'http://mse.hfut.edu.cn',
            'max_page_xpath': '//*[@class="all_pages"]/text()',
            'container_xpath': '//*[@id="wp_news_w23"]/ul',
            'time_xpath': '/*[@class="news_date"]/text()',
            'url_xpath': '/*[@class="news_menu"]/a/@href',
            'title_xpath': '//*[@class="new_name"]/text()',
            'content_id': None,
            'content_class': 'wp_articlecontent',
        },
    }
}
