## Job_spider

### 目的
    
此项目为Python练手项目，功能是爬取各种求职网上的的职位信息（包括职位名称、薪水、公司名称等），项目以爬取拉勾网上的Python职位为例

### 配置环境

* Python3
* requests
* BeautifulSoup

### 数据库设计

数据库暂定使用非关系型数据库Mongodb，它以键值对存储，结构不固定，这样每一条记录可以有不同的字段，可以少建几个关联表，方便爬虫功能的扩展

数据库的初始结构设计如下：

jobs表设计如下：


    {   
        "_id" :
        "job_title" : String
        "salary" : String
        "company" : {
            "company_name" : String
            "industry" : String
            "verified" : Bool
        }
        "location" : String
        "tag" : List String
        "welfare" : String
        "format_time" : String
    }
