## JobSpider

### 目的
    
此项目为Python练手项目，功能是爬取各种求职网上的的职位信息（包括职位名称、薪水、公司名称等），项目以爬取拉勾网上的Python职位为例

### 数据库设计

数据库暂定使用非关系型数据库Mongodb，它以键值对存储，结构不固定，这样每一条记录可以有不同的字段，可以少建几个关联表，方便爬虫功能的扩展

jobs表的设计用一个职位的爬取结果展示如下：



    {   
        "_id" :
        "job_title" : "Python开发工程师",
        "salary" : "10k-20k",
        "company" : {
            "company_name" : '顺网科技',
            "industry" : '游戏,文化娱乐 / 上市公司'
        },
        "location" : "成都·武侯区",
        "tags" : "['游戏', '直播', '中级', 'Java', '后端']",
        "welfare" : "上市公司,大数据,大平台,福利健全",
        "format_time" : 2018-03-19
    }


### 运行说明

* 环境：Python3 & requests & BeautifulSoup
* 运行： `python job_spider.py`
* 数据处理
* 将处理好的`data.csv`文件导入`mongodb`
    
    `mongoimport -d "resources" --type "csv" -c "jobs" --file=data.csv -h localhost:27017 -f "title,salary,company,location,tags,welfare,format_time"`

### 需要解决的问题
* ~~目前只能爬取前五页，所以需要写反反爬虫机制~~
* ~~需要爬取某一岗位的总页数，目前是写死的~~
* ~~目前只是把数据存入了csv文件，还需要建立数据库来存储~~
* 需要考虑到爬虫异常的处理，如网络异常等
* 分布式爬取
* ... 