Vue.use(VueResource)

Array.prototype.removeByValue = function (val) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == val) {
            this.splice(i, 1);
            break;
        }
    }
}

Array.prototype.has = function (val) {
    for (var i = 0; i < this.length; i++) {
        if (this[i] == val) {
            return true;
        }
    }
    return false;
}

var card = Vue.component('show-card', {
    props: ['info'],
    template: '#card-tpl',
    mounted: function () {
        this.getItems();
    },
    data: function() {
        return {
            items: [],
            detailUrl: '/detail/' + this.info.code,
        }
    },
    methods: {
        getItems: function() {
            baseUrl = 'http://127.0.0.1:5000/api/news/';
            this.$http.jsonp(baseUrl + this.info.code)
                .then((res) => {
                    this.items = res.data;
                })
        }
    }
});

var app = new Vue({
    el: '#app',
    data: {
        url: 'http://127.0.0.1:5000/api/unit_list',
        units: [],
        cache: [],
        currentInput: '',
    },
    mounted: function () {
        //console.log('ready');
        this.getUnits();
    },
    methods: {
        getUnits: function () {
            this.$http.jsonp(this.url)
            .then((res) => {
                // console.log(res.data);
                this.units = res.data;
                })
        },
        isShow: function (code) {
            if (this.showList.has(code))
                return true;
            return false;
        }
    },
    computed: {
        showList: function () {
            //恢复cache
            if (this.cache.length > 0)
                this.units = this.cache;
            var showList = [];
            let items = this.units
            data = []
            for (i = 0; i < items.length; i++) {
                if (items[i].name.search(this.currentInput) != -1) {
                    showList.push(items[i].code);
                    data.push(items[i]);
                    //this.units.splice(i, 1);
                }
            }
            this.units = data;
            this.cache = items;
            return showList;
        }


    }
      
});
