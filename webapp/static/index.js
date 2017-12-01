Vue.use(VueResource)

Vue.component('show-card', {
    props: ['info'],
    template: '#card-tpl',
    data: function() {
        return {
            unitInfo: this.info,
            items: [
                {
                    "id": 37,
                    "time": "17-11-27",
                    "title": "\u3010\u62a5\u544a\u8bb2\u5ea7\u3011\u4f55\u5efa\u6c11: \u521b\u4e1a\u6c99\u9f99\u4e4b\u521b\u65b0\u521b\u4e1a\u6559\u80b2\u4e0e\u5b66\u751f\u80fd\u529b\u57f9\u517b",
                    "url": "http://news.hfut.edu.cn//show-28-86482-1.html"
                },
                {
                    "id": 38,
                    "time": "17-09-20",
                    "title": "\u3010\u5408\u4f5c\u4ea4\u6d41\u3011\u4e2d\u4fe1\u57ce\u5f00\u96c6\u56e2\u603b\u7ecf\u7406\u52a9\u7406\u767d\u667a\u52c7\u4e00\u884c\u6765\u8bbf\u6211\u6821",
                    "url": "http://news.hfut.edu.cn//show-162-62066-1.html"
                },
                {
                    "id": 39,
                    "time": "17-10-24",
                    "title": "\u3010\u62a5\u544a\u8bb2\u5ea7\u3011\u7ecf\u7eac\u8bba\u575b\uff08\u4e94\uff09\u674e\u6653\u6656: \u4e09\u7ef4\u5730\u8d28\u586b\u56fe\u53ca\u6210\u77ff\u9884\u6d4b\u7814\u7a76\u4e0e\u5b9e\u8df5",
                    "url": "http://news.hfut.edu.cn//show-28-73072-1.html"
                },
                {
                    "id": 40,
                    "time": "17-10-18",
                    "title": "\u3010\u62a5\u544a\u8bb2\u5ea7\u3011\u90dd\u5929\u4f1f: Wastewater Treatment in Coastal Regions towards Resource and Energy Recovery",
                    "url": "http://news.hfut.edu.cn//show-28-72934-1.html"
                }, 
            ]
        }
    }
});

var show = new Vue({
    el: '#news-view',
    data: {
        url: 'http://118.89.48.63:88/api/unit_list',
        units : [],
        /*
        [
            {
                "code": "CI",
                "name": "\u8ba1\u7b97\u673a\u4e0e\u4fe1\u606f\u5b66\u9662",
                "tag_codes": {
                    "8": "\u5b66\u9662\u65b0\u95fb",
                    "9": "\u901a\u77e5\u516c\u544a"
                }
            },
            {
                "code": "EA",
                "name": "\u7535\u6c14\u4e0e\u81ea\u52a8\u5316\u5de5\u7a0b\u5b66\u9662",
                "tag_codes": {
                    "announcements-zh": "\u901a\u77e5\u516c\u544a",
                    "ea-academic": "\u5b66\u672f\u52a8\u6001",
                    "ea-news-zh": "\u5b66\u9662\u65b0\u95fb",
                    "ea-photonews": "\u7cbe\u9009\u56fe\u6587"
                }
            }, 
        ],*/
    },
    mounted: function () {
        console.log('ready');
        this.getUnits();
    },
    methods: {
        getUnits: function () {
            this.$http.jsonp(this.url)
            .then((response) => {
                this.$set('units', response.data)
                }).catch(function (response) {
                    console.log(response)
            })
        }
    }
      
});
